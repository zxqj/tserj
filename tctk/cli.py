from random import randint

import asyncclick as click
from twitchAPI.type import ChatEvent

from twitchAPI.chat import ChatMessage
from .bot import ChatBot
from dataclasses import dataclass

randhex = lambda d: hex(randint(0,16**d - 1)).split("x")[1].rjust(d,"0")
unique = lambda s: f"{s} {randhex(4)}"

@dataclass
class TriggerResp:
    trigger_text: str
    response: str
    trigger_username: str

def make_raffle_joiner(context: TriggerResp):
    raffle_joiner = dict()

    async def f(c: ChatBot, msg: ChatMessage):
        print(msg.user.name)
        print(msg.text)
        text_pred = lambda m: context.trigger_text in m.text
        predicate = text_pred

        if context.trigger_username is not None:
            predicate = lambda m: text_pred(m) and context.trigger_username.lower() == m.user.name.lower()
        if predicate(msg):
            await c.send_message(unique(context.response))
        print()

    raffle_joiner[ChatEvent.MESSAGE] = f
    return raffle_joiner

@click.command()
@click.option("--channel", "-c", "channel", default="thestreameast")
@click.option("--trigger-text", "--trigger", "-t", "trigger_text", default="Multi-Raffle")
@click.option("--trigger-username", "--username", "-u", "trigger_username", default="streamelements")
@click.option("--response-text", "--response", "-r", "response_text", default="!join")
async def cli(channel, trigger_text, response_text, trigger_username):
    responder = ChatBot(channel=channel)
    context = TriggerResp(trigger_text=trigger_text, response=response_text, trigger_username=trigger_username)
    features = []
    features.append(make_raffle_joiner(context))
    await responder.run(features)
