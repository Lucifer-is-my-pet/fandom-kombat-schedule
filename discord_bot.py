import discord
import conf
from discord.ext import commands
from datetime import date
import os

bot = commands.Bot(command_prefix="$", description="A bot that gives FK schedule")

# TODAY = date.today()
TODAY = date(2018, 8, 20)

QUEST_SCHEDULE = {"визитка": [date(TODAY.year, 7, 21), date(TODAY.year, 7, 22)],
                  "драбблы нерейтинг": [date(TODAY.year, 7, 26), date(TODAY.year, 7, 27)],
                  "мини нерейтинг": [date(TODAY.year, 7, 31), date(TODAY.year, 8, 1)],
                  "визуал нерейтинг": [date(TODAY.year, 8, 5), date(TODAY.year, 8, 6)],
                  "миди нерейтинг": [date(TODAY.year, 8, 10), date(TODAY.year, 8, 11)],
                  "челлендж": [date(TODAY.year, 8, 15), date(TODAY.year, 8, 16)],
                  "бб": [date(TODAY.year, 8, 26), date(TODAY.year, 8, 27)],
                  "драбблы рейтинг": [date(TODAY.year, 9, 6), date(TODAY.year, 9, 7)],
                  "мини рейтинг": [date(TODAY.year, 9, 11), date(TODAY.year, 9, 12)],
                  "визуал рейтинг": [date(TODAY.year, 9, 16), date(TODAY.year, 9, 17)],
                  "миди рейтинг": [date(TODAY.year, 9, 21), date(TODAY.year, 9, 22)],
                  "спецквест": [date(TODAY.year, 9, 26), date(TODAY.year, 9, 27)]}

LEVEL_SCHEDULE = {1: date(TODAY.year, 7, 21),
                  2: date(TODAY.year, 7, 26),
                  3: date(TODAY.year, 8, 15),
                  4: date(TODAY.year, 8, 26),
                  5: date(TODAY.year, 9, 6),
                  6: date(TODAY.year, 9, 26)}

VOTE_SCHEDULE = [
    {"name": "визитка", "beginning": date(TODAY.year, 7, 23), "end": date(TODAY.year, 8, 13),
     "out": "визитку"},
    {"name": "драбблы нерейтинг", "beginning": date(TODAY.year, 7, 28), "end": date(TODAY.year, 8, 18),
     "out": "нерейтинговые драбблы", "rating": False},
    {"name": "мини нерейтинг", "beginning": date(TODAY.year, 8, 2), "end": date(TODAY.year, 8, 23),
     "out": "нерейтинговые мини", "rating": False},
    {"name": "визуал нерейтинг", "beginning": date(TODAY.year, 8, 7), "end": date(TODAY.year, 8, 28),
     "out": "нерейтинговый визуал", "rating": False},
    {"name": "миди нерейтинг", "beginning": date(TODAY.year, 8, 12), "end": date(TODAY.year, 9, 2),
     "out": "нерейтинговые миди", "rating": False},
    {"name": "челлендж", "beginning": date(TODAY.year, 8, 17), "end": date(TODAY.year, 9, 7), "out": "челлендж"},
    {"name": "бб", "beginning": date(TODAY.year, 8, 28), "end": date(TODAY.year, 10, 19), "out": "ББ"},
    {"name": "драбблы рейтинг", "beginning": date(TODAY.year, 9, 8), "end": date(TODAY.year, 9, 29),
     "out": "рейтинговые драбблы", "rating": True},
    {"name": "мини рейтинг", "beginning": date(TODAY.year, 9, 13), "end": date(TODAY.year, 10, 4),
     "out": "рейтинговые мини", "rating": True},
    {"name": "визуал рейтинг", "beginning": date(TODAY.year, 9, 18), "end": date(TODAY.year, 10, 9),
     "out": "рейтинговый визуал", "rating": True},
    {"name": "миди рейтинг", "beginning": date(TODAY.year, 9, 23), "end": date(TODAY.year, 10, 14),
     "out": "рейтинговые миди", "rating": True},
    {"name": "спецквест", "beginning": date(TODAY.year, 9, 28), "end": date(TODAY.year, 10, 19), "out": "спецквест"}
]


def is_not_in_quest_list(word):
    if word not in QUEST_SCHEDULE.keys():
        return True
    return False


def quest_feature(quest_name, feature):
    return list(filter(lambda quest: quest["name"] == quest_name, VOTE_SCHEDULE))[0][feature]


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)


@bot.command()
async def deadline():
    await bot.say("Похуй, пляшем :dancer: :man_dancing:")


@bot.command()
async def bonus():
    await bot.say("Бонус выкладывается с 23.07 по 19.10 включительно, в дни, свободные от выкладок")


@bot.command()
async def non_comp():
    await bot.say("Внеконкурс выкладывается с 28.07 по 19.10 включительно, в дни, свободные от выкладок.\n**Не ранее "
                  "конкурсной выкладки соответствующего левела и квеста.**")


@bot.command()
async def pic():
    schedule = discord.Embed()
    schedule.set_image(url="http://funkyimg.com/i/2DVSq.png")
    await bot.say(embed=schedule)


@bot.command()
async def quest(sought_quest, *args):
    if sought_quest.find("чел") + 1:
        sought_quest = "челлендж"

    if args:
        if args[0] not in ["рейтинг", "нерейтинг"]:
            await bot.say("Квест либо рейтинговый, либо нерейтинговый, третьего не дано")
            return
        else:
            sought_quest = sought_quest + " " + args[0]

    if is_not_in_quest_list(sought_quest.lower()):
        await bot.say("Таких квестов не знаю")
        return

    quest_first_date = QUEST_SCHEDULE[sought_quest.lower()][0]
    quest_second_date = QUEST_SCHEDULE[sought_quest.lower()][1]
    quest_days_left = (quest_first_date - TODAY).days
    if quest_days_left > 0:
        await bot.say(quest_first_date.strftime("%d.%m") + "-" + quest_second_date.strftime("%d.%m") +
                      ", осталось дней до выкладки: {}".format(quest_days_left))
    else:
        await bot.say(quest_first_date.strftime("%d.%m"))


@bot.command()
async def level(level):
    try:
        level = int(level)
    except ValueError:
        await bot.say("Таких левелов не знаю, дайте цифру")
        return

    if level not in range(1, 7):
        await bot.say("Таких левелов не знаю")
        return

    level_date = LEVEL_SCHEDULE[level]
    level_delta = level_date - TODAY
    level_days_left = level_delta.days
    if level_days_left > 0:
        await bot.say(level_date.strftime("%d.%m") + ", осталось дней: {}".format(level_days_left))
    else:
        await bot.say(level_date.strftime("%d.%m"))


@bot.command()
async def vote(sought_quest: str, *args):
    if sought_quest.find("чел") + 1:
        sought_quest = "челлендж"

    if args:
        if args[0] not in ["рейтинг", "нерейтинг"]:
            await bot.say("Квест либо рейтинговый, либо нерейтинговый, третьего не дано")
            return
        else:
            sought_quest = sought_quest + " " + args[0]

    if is_not_in_quest_list(sought_quest.lower()):
        await bot.say("Таких квестов не знаю")
        return

    quest_beginning = quest_feature(sought_quest, "beginning")
    quest_end = quest_feature(sought_quest, "end")
    quest_days_left = (quest_end - TODAY).days
    quest_output = quest_feature(sought_quest, "out")

    print()
    if quest_beginning > TODAY:  # если дата начала голосования позже сегодня
        await bot.say("Голосование за {} ещё не началось".format(quest_output))
    elif quest_end < TODAY:  # если дата окончания голосования раньше сегодня
        await bot.say("Голосование за {} уже закончилось".format(quest_output))
    else:
        await bot.say("Голосование за {} закончится ".format(quest_output) + quest_end.strftime("%d.%m") +
                      ", осталось дней: {}".format(quest_days_left))


@bot.command()
async def help_():
    embed = discord.Embed(title="fandom-kombat-schedule", description="Расписание ФБ. Бот принимает команду и одно-два"
                                                                      " слова/цифру. **Команды:**", color=0xeee657)

    embed.add_field(name="$pic", value="Выводит картинку с расписанием", inline=False)
    embed.add_field(name="$quest %название% [рейтинг/нерейтинг]", value="Выводит даты выкладок для квеста"
                                                                        " **название** и оставшееся"
                                                                        " количество дней до начала, если он в будущем."
                                                                        " Пример: `$quest миди рейтинг`", inline=False)
    embed.add_field(name="$level %номер%",
                    value="Выводит дату начала левела номер **номер** и оставшееся количество дней,"
                          " если он в будущем. Пример: `$level 3`", inline=False)
    embed.add_field(name="$bonus", value="Выводит даты выкладки бонуса", inline=False)
    embed.add_field(name="$non_comp", value="Выводит даты выкладки внеконкурса", inline=False)
    embed.add_field(name="$deadline", value="Подбадривает", inline=False)
    embed.add_field(name="$vote %название% [рейтинг/нерейтинг]",
                    value="Сколько осталось до конца голосования за квест **название**."
                          " Пример: `$vote ББ`", inline=False)
    embed.add_field(name="$help_", value="Выводит эту справку", inline=False)
    embed.add_field(name="Названия квестов", value="визитка, драбблы, мини, миди, визуал,"
                                                   "челлендж (можно писать по-разному), ББ, спецквест", inline=False)
    await bot.say(embed=embed)


@bot.command()
async def start():
    await bot.say("Привет, сейчас у меня " + TODAY.strftime("%d.%m.%Y") + ", для справки вызови $help_")

bot.run(os.environ["BOT_TOKEN"])
