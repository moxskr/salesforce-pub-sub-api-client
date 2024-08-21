import asyncio
import logging
from typing import AsyncGenerator

import avro.schema
import certifi
import grpc  # type: ignore

from clients import AuthClient
from configs import GrpcConfig
from handlers import BasicHandler
from utils import process_bitmap
from utils import decode
from dtos import Event

import pubsubapi.pubsub_api_pb2 as pb2
import pubsubapi.pubsub_api_pb2_grpc as pb2_grpc

logger = logging.getLogger(__name__)


class AsyncSubscribtion:
    stub: pb2_grpc.PubSubStub
    handler: BasicHandler
    auth_metadata: tuple[tuple[str, str], ...]
    event_type: str
    schema: str = ''

    def __init__(self, stub: pb2_grpc.PubSubStub, event_type: str, handler: BasicHandler, auth_metadata: tuple[tuple[str, str], ...]) -> None:
        self.stub = stub
        self.event_type = event_type
        self.handler = handler
        self.auth_metadata = auth_metadata

    async def run(self) -> None:
        subscription_lock = asyncio.Lock()

        subscription_request = self.get_subscribe_request(subscription_lock)

        await self.subscribe_to_events(subscription_request, subscription_lock)

    async def get_subscribe_request(self, subscription_lock: asyncio.Lock) -> AsyncGenerator[pb2.FetchRequest, None]:
        while True:
            await subscription_lock.acquire()
            yield pb2.FetchRequest(
                topic_name=self.event_type,
                replay_preset=pb2.ReplayPreset.LATEST,
                num_requested=1
            )

    async def subscribe_to_events(self, subscription_request: AsyncGenerator[pb2.FetchRequest, None], subscription_lock: asyncio.Lock):
        stream = self.stub.Subscribe(
            subscription_request,
            metadata=self.auth_metadata
        )

        await self.process_events(stream, subscription_lock)

    async def process_events(self, stream: AsyncGenerator, subscription_lock: asyncio.Lock):
        async for event in stream:
            subscription_lock.release()

            if event.events:
                replay_id = int.from_bytes(event.latest_replay_id)

                logger.info(
                    f'Given an event of type {self.event_type} and replayId: {replay_id}'
                )

                if not self.schema:
                    self.schema = await self.get_schema(event)

                self.handler.process_event(
                    self.decode_event(event)
                )

    async def get_schema(self, event):
        schema_request = self.get_schema_request(event)

        result = await self.stub.GetSchema(schema_request, metadata=self.auth_metadata)

        return result.schema_json

    def get_schema_request(self, event):
        schema_id = event.events[0].event.schema_id

        return pb2.SchemaRequest(schema_id=schema_id)

    def decode_event(self, event):
        payload = event.events[0].event.payload

        decoded_payload = decode(self.schema, payload)

        return self.build_event_dto(decoded_payload)

    def build_event_dto(self, payload: dict):
        change_event_header = payload['ChangeEventHeader']
        
        change_type = change_event_header['changeType']

        changed_fields = process_bitmap(
            avro.schema.parse(self.schema),
            change_event_header['changedFields']
        )

        del payload['ChangeEventHeader']

        event = Event(
            change_type=change_type,
            changed_fields=changed_fields,
            fields=payload
        )

        return event


class AsyncPubSubClient:
    auth_client: AuthClient
    grpc_config: GrpcConfig
    event_handlers: dict[str, BasicHandler]

    def __init__(self, auth_client: AuthClient, grpc_config: GrpcConfig) -> None:
        self.auth_client = auth_client
        self.grpc_config = grpc_config
        self.event_handlers = {}

    def register_handler(self, event_type: str, event_handler: BasicHandler) -> None:
        logger.info(
            f'{type(event_handler)} handler registered for event {event_type}'
        )

        self.event_handlers[event_type] = event_handler

    async def run(self) -> None:
        try:
            auth_metadata = await self.auth_client.get_auth_metadata()
        except Exception as e:
            logger.error(f'An error occured during authorization. {e}')
        else:
            with open(certifi.where(), 'rb') as f:
                creds = grpc.ssl_channel_credentials(f.read())

            async with grpc.aio.secure_channel(self.grpc_config.full_enpoint, creds) as channel:
                stub = pb2_grpc.PubSubStub(channel)

                await self.run_subscriptions(stub, auth_metadata)

    async def run_subscriptions(self, stub: pb2_grpc.PubSubStub, auth_metadata: tuple[tuple[str, str], ...]) -> None:
        async with asyncio.TaskGroup() as tg:
            for event, handler in self.event_handlers.items():
                subscription = AsyncSubscribtion(
                    stub, event, handler, auth_metadata
                )

                logger.info(f'Subscription was created for event {event}')

                tg.create_task(subscription.run())
