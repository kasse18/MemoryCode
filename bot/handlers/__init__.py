from aiogram import Router


def setup_routers() -> Router:
    from . import user, admin

    router = Router()
    router.include_router(user.router)

    return router
