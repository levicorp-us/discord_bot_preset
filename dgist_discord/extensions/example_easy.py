import lightbulb

plugin = lightbulb.Plugin('Example2')

@plugin.command
@lightbulb.command('ping', 'says pong')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong")

def load(bot):
    bot.add_plugin(plugin)
