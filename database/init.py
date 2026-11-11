from .database import get_connection

from .emoji_limiter import init_tables as init_emoji_limiter
from .reaction_roles import init_tables as init_reaction_roles
from .link_players import init_tables as init_linked_players
from .command_channels import init_tables as init_command_channels
from .languages import init_tables as init_languages


INITIALIZERS = (
    init_emoji_limiter,
    init_reaction_roles,
    init_linked_players,
    init_command_channels,
    init_languages,
)


def init_database() -> None:
    with get_connection() as connection:
        for initializer in INITIALIZERS:
            initializer(connection)