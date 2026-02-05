import asyncclick as click
from .cli_tools import loudspeaker, wrap_module_with_decorator
import asyncio
from .bot import ChatResponder

loud_sh = wrap_module_with_decorator('sh', loudspeaker)

@click.command()
@click.option("--channel", "-c", "channel", default="thestreameast")
@click.option("--trigger-text", "--trigger", "-t", "trigger_text", default="Multi-Raffle")
@click.option("--trigger-username", "--username", "-u", "trigger_username", default="streamelements")
@click.option("--response-text", "--response", "-r", "response_text", default="!join")
async def cli(channel, trigger_text, response_text, trigger_username):
    responder = ChatResponder(channel=channel,
                              trigger_text=trigger_text,
                              response=response_text,
                              trigger_username=trigger_username)
    await responder.run()
