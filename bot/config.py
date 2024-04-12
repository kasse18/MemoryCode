import os
from dataclasses import dataclass
from environs import Env


@dataclass
class BotConfig:
    token: str
    pay_token: str
    admin_ids: list[int]


@dataclass
class DbConfig:
    db_user_name: str = str(os.getenv('DB_USER_NAME'))
    db_user_password: str = str(os.getenv('DB_USER_PASSWORD'))
    db_host: str = str(os.getenv('DB_HOST'))
    db_port: str = str(os.getenv('DB_PORT'))
    db_name: str = str(os.getenv('DB_NAME'))


@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


env: Env = Env()
env.read_env()

config = Config(
    bot=BotConfig(
        token=env('BOT_TOKEN', None),
        pay_token=env('PAY_TOKEN', None),
        admin_ids=list(map(int, env.list('ADMIN_IDS')))
    ),
    db=DbConfig(
        db_user_name=env('DB_USER_NAME', None),
        db_user_password=env('DB_USER_PASSWORD', None),
        db_host=env('DB_HOST', None),
        db_port=env('DB_PORT', None),
        db_name=env('DB_NAME', None)
    )
)

print(config.bot)
print(config.db)
