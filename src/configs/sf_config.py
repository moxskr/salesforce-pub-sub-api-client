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