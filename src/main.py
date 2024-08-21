import asyncio
import logging

from clients import AsyncPubSubClient, NotificationClientImpl, SfAuthClient
from configs import get_sf_auth_config, get_sf_grpc_config
from handlers import CaseHandler
from services import CaseServiceImpl


async def main():
    auth_client = SfAuthClient(auth_config=get_sf_auth_config())

    pub_sub_client = AsyncPubSubClient(
        auth_client=auth_client,
        grpc_config=get_sf_grpc_config()
    )
    
    notification_client = NotificationClientImpl()
    
    case_service = CaseServiceImpl()

    case_handler = CaseHandler(
        case_service=case_service,
        notification_client=notification_client
    )

    pub_sub_client.register_handler(
        '/data/CaseChangeEvent',
        case_handler
    )

    await pub_sub_client.run()


if __name__ == '__main__':
    logging.basicConfig(
        filename='logs/pubsubapi.log',
        level=logging.INFO,
        format='[%(levelname)s]|[%(asctime)s]|%(name)s -  - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger(__name__)
    
    logger.info('Starting Event Loop')

    asyncio.run(main())
