import lightbulb
import hikari
import asyncio

plugin = lightbulb.Plugin('Example')

psr_map = {
    '✌️' : 1,
    '👊' : 2,
    '🖐️' : 3,
}

accept = False

def evaluate(res1 : int, res2 : int)->int:
    if res1 == res2:
        return 0
    elif any([res1 == res2 + 1, res1 == 1 and res2 == 3, res2 == 0]):
        return 1
    elif any([res2 == res1 + 1, res2 == 1 and res1 == 3, res1 == 0]):
        return 2

def check_userid(id : str)->bool:
    return all([
        id[0:2] == "<@",
        id[-1] == ">",
        len(id) <= 21,
    ])

async def paperscissorsrock(ctx : lightbulb.context, userid:str)->None:
    targetchannel = await ctx.bot.rest.create_dm_channel(userid)
    
    def check(event: hikari.ReactionAddEvent):
        valid = all([
            str(event.user_id) == str(userid),
            str(event.emoji_name) in ["✌️","👊","🖐️"],
        ])
        return valid
    
    embed_options = (
        hikari.Embed(
        title="가위바위보!!!",
        description="가위, 바위, 보 중 하나를 고르세요"
        )
    )
    
    msg = await targetchannel.send(embed=embed_options)
    await msg.add_reaction("✌️")
    await msg.add_reaction("👊")
    await msg.add_reaction("🖐️")
    
    try:
        event = await ctx.bot.wait_for(hikari.ReactionAddEvent, timeout=30, predicate=check)
        await targetchannel.send("가위, 바위, 보 중에 "+event.emoji_name+"을(를) 선택했군요!")
        return psr_map[event.emoji_name]
    except asyncio.TimeoutError:
        await targetchannel.send("시간 안에 안 내셨기에 패배로 결정됩니다")
        return 0

@plugin.command
@lightbulb.option('opponent', '상대를 @로 지목하세요', required=True, type=str)
@lightbulb.command('가위바위보', '지목한 상대와 가위바위보를 합니다', ephemeral=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def paper_scissors_rock(ctx: lightbulb.context):
    if str(ctx.author.id) == ctx.options.opponent[2:-1]:
        await ctx.respond("자기 자신과 가위바위보를 할 수는 없습니다")
        return
    elif not check_userid(str(ctx.options.opponent)):
        print(ctx.options.opponent)
        await ctx.respond("올바른 상대를 지목하세요")
        return
    
    await ctx.respond("<@"+str(ctx.author.id)+">"+" vs "+ctx.options.opponent+"의 가위바위보 대결!!!")        
    
    tasks = [
        paperscissorsrock(ctx, ctx.author.id), 
        paperscissorsrock(ctx, ctx.options.opponent[2:-1])
    ]
    res = await asyncio.gather(*tasks)
    
    result = evaluate(res[0], res[1])
    
    if result == 0:
        await ctx.respond("<@"+str(ctx.author.id)+"> "+ ctx.options.opponent +" 무승부!!!")
    elif result == 1:
        await ctx.respond("<@"+str(ctx.author.id)+">의 승리, " + ctx.options.opponent + "의 패배!!!")
    elif result == 2:
        await ctx.respond(ctx.options.opponent + "의 승리, " + "<@"+str(ctx.author.id)+">" + "의 패배!!!")
    
    
    
def load(bot):
    bot.add_plugin(plugin)