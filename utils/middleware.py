from functools import wraps
from typing import Tuple, Coroutine, Callable, Type
import discord

def has_any_role(*roles: Tuple[str]) -> Callable:
    def decorator(func: Coroutine) -> Coroutine:
        @wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            if not isinstance(interaction.user, discord.Member):
                return await interaction.response.send_message('Something went wrong!', ephemeral=True)

            user_roles = {role.name for role in interaction.user.roles}
            for role in roles:
                if role in user_roles:
                    return await func(self, interaction, *args, **kwargs)

            await interaction.response.send_message("You don't have the permission to execute this command!", ephemeral=True)
        return wrapper
    return decorator

def handle_errors(*errors: Type[Exception]) -> Callable:
    def decorator(func: Coroutine) -> Coroutine:
        @wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            try:
                await func(self, interaction, *args, **kwargs)
            except errors as error:
                await interaction.response.send_message(error, ephemeral=True)
        return wrapper
    return decorator