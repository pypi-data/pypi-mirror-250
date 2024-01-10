"""A command handler for hikari.

To get started, see the following links:

GitHub:
https://github.com/hypergonial/hikari-arc
Documentation:
https://arc.hypergonial.com
"""

from alluka import Client as Injector
from alluka import inject

from arc import abc, command, utils

from .abc import HookResult, Option, OptionType, with_hook, with_post_hook
from .client import (
    Client,
    GatewayClient,
    GatewayClientBase,
    GatewayContext,
    GatewayPlugin,
    RESTClient,
    RESTClientBase,
    RESTContext,
    RESTPlugin,
)
from .command import (
    AttachmentParams,
    BoolParams,
    ChannelParams,
    FloatParams,
    IntParams,
    MentionableParams,
    MessageCommand,
    RoleParams,
    SlashCommand,
    SlashGroup,
    SlashSubCommand,
    SlashSubGroup,
    StrParams,
    UserCommand,
    UserParams,
    message_command,
    slash_command,
    slash_subcommand,
    user_command,
)
from .context import AutocompleteData, AutodeferMode, Context, InteractionResponse
from .errors import (
    ArcError,
    AutocompleteError,
    CommandInvokeError,
    CommandPublishFailedError,
    DMOnlyError,
    GuildCommandPublishFailedError,
    GuildOnlyError,
    InvokerMissingPermissionsError,
    NotOwnerError,
    UnderCooldownError,
)
from .events import ArcEvent, CommandErrorEvent
from .extension import loader, unloader
from .internal.about import __author__, __author_email__, __license__, __maintainer__, __url__, __version__
from .locale import (
    CommandLocaleRequest,
    CustomLocaleRequest,
    LocaleRequest,
    LocaleRequestType,
    LocaleResponse,
    OptionLocaleRequest,
)
from .plugin import GatewayPluginBase, PluginBase, RESTPluginBase
from .utils import (
    bot_has_permissions,
    channel_limiter,
    custom_limiter,
    dm_only,
    global_limiter,
    guild_limiter,
    guild_only,
    has_permissions,
    member_limiter,
    owner_only,
    user_limiter,
)

__all__ = (
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__url__",
    "__maintainer__",
    "AutodeferMode",
    "inject",
    "Injector",
    "AutocompleteData",
    "Option",
    "Context",
    "Context",
    "BoolParams",
    "IntParams",
    "StrParams",
    "FloatParams",
    "UserParams",
    "ChannelParams",
    "RoleParams",
    "MentionableParams",
    "AttachmentParams",
    "SlashCommand",
    "SlashGroup",
    "SlashSubCommand",
    "SlashSubGroup",
    "MessageCommand",
    "UserCommand",
    "message_command",
    "user_command",
    "slash_command",
    "slash_subcommand",
    "Client",
    "GatewayClientBase",
    "RESTClientBase",
    "GatewayClient",
    "RESTClient",
    "OptionType",
    "ArcError",
    "AutocompleteError",
    "UnderCooldownError",
    "InvokerMissingPermissionsError",
    "GuildOnlyError",
    "NotOwnerError",
    "DMOnlyError",
    "CommandInvokeError",
    "GuildCommandPublishFailedError",
    "CommandPublishFailedError",
    "PluginBase",
    "RESTPluginBase",
    "GatewayPluginBase",
    "loader",
    "unloader",
    "ArcEvent",
    "CommandErrorEvent",
    "InteractionResponse",
    "GatewayContext",
    "RESTContext",
    "RESTPlugin",
    "GatewayPlugin",
    "HookResult",
    "LocaleRequest",
    "LocaleRequestType",
    "LocaleResponse",
    "CustomLocaleRequest",
    "CommandLocaleRequest",
    "OptionLocaleRequest",
    "abc",
    "utils",
    "command",
    "with_hook",
    "with_post_hook",
    "bot_has_permissions",
    "dm_only",
    "guild_only",
    "has_permissions",
    "owner_only",
    "global_limiter",
    "guild_limiter",
    "channel_limiter",
    "user_limiter",
    "member_limiter",
    "custom_limiter",
)

# MIT License
#
# Copyright (c) 2023-present hypergonial
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
