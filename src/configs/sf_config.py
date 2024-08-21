from dataclasses import dataclass
import dotenv

env_config = dotenv.dotenv_values('.env')

@dataclass
class AuthConfig:
    client_id: str
    client_secret: str
    auth_endpoint: str


@dataclass
class GrpcConfig:
    grpc_endpoint: str
    grpc_port: str

    @property
    def full_enpoint(self) -> str:
        return f'{self.grpc_endpoint}:{self.grpc_port}'


def get_sf_auth_config():
    return AuthConfig(
        client_id=env_config['SF_CLIENT_ID'],
        client_secret=env_config['SF_CLIENT_SECRET'],
        auth_endpoint=env_config['SF_AUTH_ENDPOINT']
    )


def get_sf_grpc_config():
    return GrpcConfig(
        grpc_endpoint=env_config['SF_PUBSUB_ENDPOINT'],
        grpc_port=env_config['SF_PUBSUB_PORT']
    )
