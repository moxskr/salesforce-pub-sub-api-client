import logging.config

from dependency_injector import containers, providers

from clients import SfAuthClient, AsyncPubSubClient, NotificationClientImpl
from configs import AuthConfig, GrpcConfig
from handlers import CaseHandler
from services import CaseServiceImpl


class Container(containers.DeclarativeContainer):
    # configs

    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    sf_auth_config = providers.Singleton(
        AuthConfig,
        client_id=config.sf_auth.sf_client_id,
        client_secret=config.sf_auth.sf_client_secret,
        auth_endpoint=config.sf_auth.sf_auth_endpoint
    )

    sf_grpc_config = providers.Singleton(
        GrpcConfig,
        grpc_endpoint=config.sf_grpc.sf_grpc_endpoint,
        grpc_port=config.sf_grpc.sf_grpc_port
    )

    # clients

    auth_client = providers.Singleton(
        SfAuthClient,
        auth_config=sf_auth_config
    )

    pub_sub_client = providers.Singleton(
        AsyncPubSubClient,
        auth_client=auth_client,
        grpc_config=sf_grpc_config
    )

    notification_client = providers.Singleton(
        NotificationClientImpl
    )

    # handlers and services

    case_service = providers.Factory(
        CaseServiceImpl
    )

    case_handler = providers.Factory(
        CaseHandler,
        case_service=case_service,
        notification_client=notification_client
    )