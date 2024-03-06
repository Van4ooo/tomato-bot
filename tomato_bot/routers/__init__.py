from aiogram import Router

from .routers import *
from .timer import *


main_router = Router(name=__name__)

main_router.include_routers(
    main_command_router,
    timer_router
)

__all__ = ("main_router",)
