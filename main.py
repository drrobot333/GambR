import discord, time, random
import gamble, user
import datetime
from discord.ext import commands, tasks
import asyncio

isFight = 0
count = 0
MIN = 3
peopleList = []
matchInfo = []
test = 0

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) #봇이 실행되면 콘솔창에 표시
           
@bot.command()
async def 매치(ctx):
    global isFight, count,peopleList, matchInfo
    if isFight != 1:
        peopleList = []
        year, month, day, hour, minute, second = time.localtime()[0:6]
        p1Name, p2Name = gamble.returnName()
        p1Value, tieValue, p2Value,  = gamble.returnValue()
        matchInfo = [p1Name, "무승부", p2Name, p1Value, tieValue, p2Value]
        embed = gamble.returnEmbed(year, month, day, hour, minute, p1Name, p1Value, p2Name, p2Value, tieValue, MIN)
        await ctx.send(embed = embed)
        isFight = 1
        await asyncio.sleep(60*(MIN-1))

        embed = gamble.returnAlert("⚠알림⚠", "배팅 시간이 1분 남았습니다.")
        await ctx.send(embed = embed)

        await asyncio.sleep(60*(MIN-2))

        embed = gamble.returnAlert("⚠알림⚠", "배팅이 종료되었습니다.")
        await ctx.send(embed = embed)
        
        winList, loseList, winner = user.returnResult(peopleList, matchInfo)
        strWinList, strLoseList = gamble.returnStrList(winList),  gamble.returnStrList(loseList)
        embed = discord.Embed(title = "⚔MATCH 종료!!⚔")
        embed.add_field(name = "승자", value = "{}".format(winner), inline = False)
        embed.add_field(name = "적중 성공😝", value = "{}".format(strWinList), inline = True)
        embed.add_field(name = "적중 실패😥", value = "{}".format(strLoseList), inline = True)
        await ctx.send(embed = embed)
        
        isFight = 0
        peopleList = []
        matchInfo = []
        
    else:
        embed = gamble.returnAlert("⚠알림⚠", "이미 매치가 진행중입니다.")
        await ctx.send(embed = embed)

        

@bot.command()
async def 배팅(ctx, *arg):
    if len(arg) < 2:
        embed = gamble.returnAlert("⚠\"!배팅\" 사용법⚠", "!배팅 이름 돈\nex) !배팅 김수환 1000")
        await ctx.send(embed = embed)
        return
        
    who, money = arg
    global peopleList, matchInfo
    if isFight == 1:
        if who in matchInfo:
            userID = str(ctx.author.id)
            if user.chkUser(userID):
                result = user.batPossible(userID, int(money))
                if result == "MS":
                    embed = gamble.returnMoneyAlert(ctx.author.name, user.returnMoney(userID))
                    await ctx.send(embed = embed)
                    
                elif result == "ME":
                    msg = "{}님 1원 이상 배팅 가능합니다.\n배팅 가능 금액: {}원".format(ctx.author.name, user.returnMoney(userID))
                    embed = gamble.returnAlert("⚠알림⚠", msg)
                    await ctx.send(embed =embed)
                    
                elif result == "MF":
                    user.bat(userID, int(money))
                    peopleList = user.returnPeopleList(peopleList, [ctx.author.name, userID, who,int(money)])
                    embed = gamble.returnBatAlert(ctx.author.name, who, int(money), user.returnMoney(userID), matchInfo[matchInfo.index(who)+3])
                    await ctx.send(embed = embed)

            else:
                user.addUser(ctx)
                embed = gamble.returnAlert("☑등록 성공☑", "{}님 등록되셨습니다.".format(ctx.author.name))
                await ctx.send(embed = embed)
                result = user.batPossible(userID, int(money))
                if result == "MS":
                    embed = gamble.returnMoneyAlert(ctx.author.name, user.returnMoney(userID))
                    await ctx.send(embed = embed)
                    
                elif result == "ME":
                    msg = "{}님 1원 이상 배팅 가능합니다.\n배팅 가능 금액: {}원".format(ctx.author.name, user.returnMoney(userID))
                    embed = gamble.returnAlert("⚠알림⚠", msg)
                    await ctx.send(embed =embed)
                    
                elif result == "MF":
                    user.bat(userID, int(money))
                    peopleList = user.returnPeopleList(peopleList, [ctx.author.name, userID, who,int(money)])
                    embed = gamble.returnBatAlert(ctx.author.name, who, int(money), user.returnMoney(userID), matchInfo[matchInfo.index(who)+3])
                    await ctx.send(embed = embed)
        else:
            embed = gamble.returnAlert("⛔잘못된 배팅⛔", "배팅 가능한 선수:{},{},{}".format(matchInfo[0],matchInfo[1],matchInfo[2]))
            await ctx.send(embed = embed)
    else:
        embed = gamble.returnAlert("⚠알림⚠", '현재 진행중인 매치가 없습니다.')
        await ctx.send(embed =embed)

@bot.command()
async def 보내기(ctx, *arg):
    if len(arg) < 2:
        embed = gamble.returnAlert("⚠\"!보내기\" 사용법⚠", "!보내기 이름 돈\nex) !보내기 bsj100 1000")
        await ctx.send(embed =embed)
        return
        
        
    who, money = arg
    if user.chkUser(str(ctx.author.id)): # 보내는 사람은 존재
        
        if user.chkUserByReal(who): # id에 받는사람 있으면
            numID1 = user.findUser(str(ctx.author.id))
            numID2 = user.findUserByReal(who) 
            result = user.loan(numID1, numID2, int(money))

            if result == "MS":
                embed = gamble.returnAlert("⛔머니 부족⛔", "{}\n송금 가능 금액: {}원".format(ctx.author.name, user.returnMoney(str(ctx.author.id))))
                await ctx.send(embed = embed)

            elif result == "A":
                embed = gamble.returnLoan(ctx.author.name, who, money)
                await ctx.send(embed = embed)

        else:
            embed = gamble.returnAlert("⚠사용자 오류⚠", "{}님은 존재하지 않는 사용자입니다.".format(who))
            await ctx.send(embed = embed)

    else:
        embed = gamble.returnAlert("⚠사용자 오류⚠", "{}님은 등록되지 않은 사용자입니다. 배팅에 참여하거나 !등록을 입력하면 자동으로 등록됩니다.".format(ctx.author.name))
        await ctx.send(embed = embed)
    
@bot.command()
async def 내정보(ctx):
    if user.chkUser(str(ctx.author.id)):
        money, lost, win, profit = user.info(str(ctx.author.id))
        embed = gamble.returnAlert("{}님 정보".format(ctx.author.name), "남은 돈: {}\n순수익금: {}\n적중 횟수: {}\n틀린 횟수: {}".format(money, profit, win, lost))
        await ctx.send(embed = embed)

    else:
        embed = gamble.returnAlert("⚠사용자 오류⚠", "{}님은 등록되지 않은 사용자입니다. 배팅에 참여하거나 !등록을 입력하면 자동으로 등록됩니다.".format(ctx.author.name))
        await ctx.send(embed = embed)

@bot.command()
async def 등록(ctx):
    userID = str(ctx.author.id)
    if not user.chkUser(userID):
        user.addUser(ctx)
        embed = gamble.returnAlert("☑등록 성공☑", "{}님 등록되셨습니다.".format(ctx.author.name))
        await ctx.send(embed = embed)

    else:
        embed = gamble.returnAlert("⚠사용자 오류⚠", "{}님은 이미 등록되어 있습니다".format(ctx.author.name))
        await ctx.send(embed = embed)
    

@bot.command()
async def 배팅정보(ctx):
    global peopleList, matchInfo
    win = []
    tie = []
    los = []
    if isFight == 1:
        win, tie, los = user.returnStatus(peopleList, matchInfo)
        strWinList, strTieList, strLoseList = gamble.returnStrListStatus(win),  gamble.returnStrListStatus(tie), gamble.returnStrListStatus(los)
        embed = discord.Embed(title = "⚔현재 배팅 상황⚔")
        embed.add_field(name = "{}".format(matchInfo[0]), value = "{}".format(strWinList), inline = True)
        embed.add_field(name = "{}".format(matchInfo[1]), value = "{}".format(strTieList), inline = True)
        embed.add_field(name = "{}".format(matchInfo[2]), value = "{}".format(strLoseList), inline = True)
        await ctx.send(embed = embed)

    else:
        embed = gamble.returnAlert("⚠알림⚠", '현재 진행중인 매치가 없습니다.')
        await ctx.send(embed =embed)

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "✨도움✨")
    embed.add_field(name = "!매치", value = "매치를 시작합니다.\nex) !매치",inline = False)
    embed.add_field(name = "!배팅", value = "매치 선수들에게 배팅합니다.\n!배팅 이름 돈\nex) !배팅 김수환 1000",inline = False)
    embed.add_field(name = "!보내기", value = "사용자끼리 게임머니를 송금할 수 있습니다.\n!보내기 이름 돈\nex) !보내기 bsj100 1000",inline = False)
    embed.add_field(name = "!내정보", value = "내정보를 출력해줍니다.\nex) !내정보",inline = False)
    embed.add_field(name = "!등록", value = "게임에 가입할 수 있습니다.\nex) !등록",inline = False)
    embed.add_field(name = "!배팅정보", value = "매치가 진행중일 때 배팅 정보를 확인할 수 있습니다.\nex) !등록",inline = False)

    await ctx.send(embed =embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = gamble.returnAlert("⚠명령어 오류⚠", "\"!도움\"을 입력하여 명령어를 확인하세요.")
        await ctx.send(embed = embed)

bot.run('ODY2NTc4OTQzNTY5NTU5NTUy.YPUmiA.e71obb8wpzmHjjMLde8W2w-TX6g') #토큰
