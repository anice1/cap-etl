import sshtunnel
from .env_handler import env
from sqlalchemy import create_engine

DB_HOST = env("DB", "DB_HOST")
DB_PORT = env("DB", "DB_PORT")
DB_DATABASE = env("DB", "DB_DATABASE")
DB_USERNAME = env("DB", "DB_USERNAME")
DB_PASSWORD = env("DB", "DB_PASSWORD")

SSH_PASSWORD = env("SSH", "SSH_PASSWORD")
SSH_USERNAME = env("SSH", "SSH_USERNAME")
REMOTE_IP_ADDRESS = env("SSH", "REMOTE_IP_ADDRESS")


# SQL_ALCHEMY_DB_URL = (
#     "mysql://"
#     + DB_USERNAME
#     + ":"
#     + DB_PASSWORD
#     + "@"
#     + DB_HOST
#     + ":"
#     + DB_PORT
#     + "/"
#     + DB_DATABASE
# )

SQL_ALCHEMY_DB_URL = (
    f"mysql+mysqldb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)
# "mysql+ssh: // forge@161.35.108.195/forge@127.0.0.1/forge?name=hollow-cavern & usePrivateKey=true"


def start_server():
    global server
    server = sshtunnel.SSHTunnelForwarder(
        ssh_address_or_host=(REMOTE_IP_ADDRESS),
        ssh_password=SSH_PASSWORD,
        ssh_username=SSH_USERNAME,
        remote_bind_address=(DB_HOST, DB_PORT),
    )

    server.start()
    print("Server connected successfully")
    engine = create_engine(url=SQL_ALCHEMY_DB_URL, pool_recycle=280)
    return engine


def stop_server():
    server.stop()
    print("Server stopped.")
