import random, discord

people = ['김수환', '백승재', '정인서', '이성훈', '노혜린', '김태현', '김찬우', '김호준','박지원','문범식', '황성훈', '박건하', '주상현', '최원석']

def multiPlayer(x):
    return round(20*((x-0.3)**2)+1.1 ,2)

def multiTie(x):
    return round(20*((x-0.3)**2)+2.0 ,2)

def returnName():
    return random.sample(people, 2)

def returnValue():
    return [multiPlayer(random.random()), multiTie(random.random()), multiPlayer(random.random())]

def returnEmbed(year, month, day, hour, minute, p1Name, p1Value, p2Name, p2Value, tieValue, MIN):
    embed = discord.Embed(title = "⚔{}년 {}월 {}일 {}시 {}분 MATCH!!⚔".format(year, month, day, hour, minute))
    embed.add_field(name = p1Name, value = "⬇\n{}".format(p1Value), inline = True)
    embed.add_field(name = "⚔", value = "무승부\n{}".format(tieValue), inline = True)
    embed.add_field(name = p2Name, value = "⬇\n{}".format(p2Value), inline = True)

    return embed

def returnStrList(l):
    string = ''
    if len(l) > 0:
        for i in range(len(l)):
            if l[i][1] > 0:
                string += (l[i][0] + ' +'+str(l[i][1]) +"원\n")

            else:
                string += (l[i][0] + ' '+str(l[i][1]) +"원\n")

        return string
    else:
        return "없음"

def returnStrListStatus(l):
    string = ''
    if len(l) > 0:
        for i in range(len(l)):
            string += (l[i][0] + ' '+str(l[i][1]) +"원\n")



        return string
    else:
        return "없음"

def returnAlert(title, msg):
    embed = discord.Embed(title = "{}".format(title))
    #embed.add_field(name = "{}".format(msg), value='')
    embed.add_field(name = '{}'.format(msg), value= "\u200b")
    return embed

def returnMoneyAlert(name, money):
    embed = discord.Embed(title = "⛔경고⛔")
    embed.add_field(name = '{}님 게임 머니가 부족합니다.\n배팅 가능 금액: {}원'.format(name, money), value= "\u200b")
    return embed


def returnBatAlert(name, who, money, restMoney, value):
    embed = discord.Embed(title = "💰배팅 성공💰")
    embed.add_field(name = '{}'.format(name), value= "배팅 선수: {}\n배팅 금액: {}\n예상 상금: {}\n남은 머니: {}".format(who, money,int(money*value), restMoney ), inline = False)
    '''embed.add_field(name = '배팅: {}'.format(who), value= "\u200b", inline = False)
    embed.add_field(name = '배팅금액: {}'.format(money), value= "\u200b", inline = False)
    embed.add_field(name = '예상상금: {}'.format(int(money*value)), value= "\u200b", inline = False)
    embed.add_field(name = '남은 돈: {}'.format(restMoney), value= "\u200b", inline = False)'''
    return embed

def returnLoan(name1, name2, money):
    embed = discord.Embed(title = "🤑보내기 성공🤑")
    embed.add_field(name = '{} ➡ {}\n금액: {}원'.format(name1, name2, money), value= "\u200b")
    return embed
    
