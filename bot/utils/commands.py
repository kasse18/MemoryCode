from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начало работы"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        ),
        BotCommand(
            command="order",
            description="Заполнить анкету"
        ),
        BotCommand(
            command="order",
            description="Сгенерировать эпитафию"
        ),
        BotCommand(
            command="order",
            description="Сгенерировать биографию"
        ),
        BotCommand(
            command="profile",
            description="Мой профиль"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
