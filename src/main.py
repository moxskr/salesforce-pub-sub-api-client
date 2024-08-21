import asyncio

from dependency_injector.wiring import inject, Provide

from container import Container

from clients import AsyncPubSubClient
from handlers import CaseHandler


@inject
def main(
    pub_sub_client: AsyncPubSubClient = Provide[Container.pub_sub_client],
    case_handler: CaseHandler = Provide[Container.case_handler]
):
    pub_sub_client.register_handler(
        '/data/CaseChangeEvent',
        case_handler
    )

    asyncio.run(pub_sub_client.run())


if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
