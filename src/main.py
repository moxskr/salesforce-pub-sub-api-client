import asyncio

from dependency_injector.wiring import inject, Provide

from container import Container

from clients import AsyncPubSubClient
from handlers import CaseHandler
from handlers.dispatcher import Dispatcher


@inject
def main(
    pub_sub_client: AsyncPubSubClient = Provide[Container.pub_sub_client]
):
    asyncio.run(pub_sub_client.run())


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
