from typing import Optional, Callable, Awaitable, Any, TypeAlias

from twitchAPI.twitch import Twitch
from twitchAPI.chat import Chat, ChatEvent, ChatCommand, ChatMessage, EventData
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from .config import Config
import asyncio
# Define your Client ID, Client Secret, bot username, and channel name

# Define the required scopes
async def get_chat(conf: Config = Config.get()) -> Chat:
    # Set up twitch API instance and add user authentication
    twitch = await Twitch(conf.app.id, conf.app.secret)
    auth = UserAuthenticator(twitch, conf.scopes)
    token, refresh_token = await auth.authenticate()
    Config.persist_with(access_token=token, refresh_token=refresh_token)
    await twitch.set_user_authentication(token, conf.scopes, refresh_token)

    # Create chat instance
    chat = await Chat(twitch)
    return twitch, chat

class ChatBot:
    def __init__(self, channel: str):
        self.channel = channel
        self.chat = None

    async def _delayed_send(self, channel: str, text: str, delay: float = 1.0):
        await asyncio.sleep(delay)
        if self.chat is not None:
            await self.chat.send_message(channel, text)

    async def send_message(self, text: str, delay: float = 1.0):
        await asyncio.create_task(self._delayed_send(self.channel, text, delay))

    # Main function to run the bot
    async def run(self, features: list[dict[ChatEvent, Callable[[ChatBot, EventData], Awaitable[Any]]]]):
        twitch, chat = await get_chat()
        self.chat = chat

        def make_awaitable(f: Callable[[ChatBot, EventData], Awaitable[Any]]) -> Callable[[EventData], Awaitable[Any]]:
            async def awaitable(evt: EventData):
                await f(self, evt)
            return awaitable

        for feature in features:
            for event, handler in feature.items():
                chat.register_event(event, make_awaitable(handler))

        # Connect and join the channel
        chat.start()
        await chat.join_room(self.channel)

        print('Bot is running. Press ENTER to stop.')
        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(None, input)
        finally:
            # Stop the bot and close the connection
            chat.stop()
            await twitch.close()