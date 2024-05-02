import os
import lightbulb
import hikari

if __name__ == "__main__":
    from main_bot import GUILD_ID, _token
    bot = lightbulb.BotApp(
    token = _token,
    prefix="!",
    default_enabled_guilds=[GUILD_ID, 1152810245098307677],
    intents = hikari.Intents.ALL,
    ignore_bots=True,
    )

    # bot.load_extensions('extensions.example') # specific extensions available
    bot.load_extensions_from('./extensions') # add extensions in the dir
    
    if os.name != "nt":
        import uvloop
        uvloop.install()
    
    bot.run()