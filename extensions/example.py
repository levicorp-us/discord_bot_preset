import lightbulb
import hikari
import random

from main_bot import _token

plugin = lightbulb.Plugin('Example3')

def prob_generator():
    return random.randint(0,100)

@plugin.listener(hikari.GuildMessageCreateEvent)
async def probability(event : hikari.GuildMessageCreateEvent):
    channel_id = event.channel_id
    msg = event.content
    if msg [-2:]=="확률" and msg[0] == "!":
        await event.message.respond(content="그럴 확률은 " +str(prob_generator())+ "%라고 봐")
    

def load(bot):
    bot.add_plugin(plugin)
