import discord
import conf
from discord.ext import commands
from datetime import date

bot = commands.Bot(command_prefix="$", description="A bot that gives FK schedule")

#today = date.today()
today = date(2018, 8, 20)

quest_schedule = {"визитка": [date(today.year, 7, 21), date(today.year, 7, 22)],
			"челлендж": [date(today.year, 8, 15), date(today.year, 8, 16)],
			"бб": [date(today.year, 8, 26), date(today.year, 8, 27)],
			"спецквест": [date(today.year, 9, 26), date(today.year, 9, 27)]}

level_schedule = {1: date(today.year, 7, 21),
            2: date(today.year, 7, 26),
            3: date(today.year, 8, 15),
            4: date(today.year, 8, 26),
            5: date(today.year, 9, 6),
            6: date(today.year, 9, 26)}			
			
vote_schedule = [
			{"name": "визитка", "beginning": date(today.year, 7, 23), "end": date(today.year, 8, 13), "out": "визитку"},
			{"name": "драбблы", "beginning": date(today.year, 7, 28), "end": date(today.year, 8, 18), "out": "драбблы", "rating": False},
			{"name": "мини", "beginning": date(today.year, 8, 2), "end": date(today.year, 8, 23), "out": "мини", "rating": False},
			{"name": "визуал", "beginning": date(today.year, 8, 7), "end": date(today.year, 8, 28), "out": "визуал", "rating": False},
			{"name": "миди", "beginning": date(today.year, 8, 12), "end": date(today.year, 9, 2), "out": "миди", "rating": False},
			{"name": "челлендж", "beginning": date(today.year, 8, 17), "end": date(today.year, 9, 7), "out": "челлендж"},
			{"name": "бб", "beginning": date(today.year, 8, 28), "end": date(today.year, 10, 19), "out": "ББ"},
			{"name": "драбблы", "beginning": date(today.year, 9, 8), "end": date(today.year, 9, 29), "out": "драбблы", "rating": True},
			{"name": "мини", "beginning": date(today.year, 9, 13), "end": date(today.year, 10, 4), "out": "мини", "rating": True},
			{"name": "визуал", "beginning": date(today.year, 9, 18), "end": date(today.year, 10, 9), "out": "визуал", "rating": True},
			{"name": "миди", "beginning": date(today.year, 9, 23), "end": date(today.year, 10, 14), "out": "миди", "rating": True},
			{"name": "спецквест", "beginning": date(today.year, 9, 28), "end": date(today.year, 10, 19), "out": "спецквест"}
			]

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
    await bot.say("Внеконкурс выкладывается с 28.07 по 19.10 включительно, в дни, свободные от выкладок.\n**Не ранее конкурсной выкладки соответствующего левела и квеста.**")	
	
@bot.command()
async def schedule():
    schedule = discord.Embed()
    schedule.set_image(url="http://funkyimg.com/i/2DVSq.png")
    await bot.say(embed=schedule)

@bot.command()
async def quest(sought_quest):
	if sought_quest.find("чел") + 1:
		sought_quest = "челлендж"
	
	quests = set(map(lambda quest: quest["name"], vote_schedule))
	if sought_quest.lower() not in quests:
		await bot.say("Таких квестов не знаю")
		return
	
	quest_first_date = quest_schedule[sought_quest.lower()][0]
	quest_second_date = quest_schedule[sought_quest.lower()][1]
	quest_delta = quest_first_date - today
	quest_days_left = quest_delta.days
	if quest_days_left > 0:
		await bot.say(quest_first_date.strftime("%d.%m") + "-" + quest_second_date.strftime("%d.%m") + ", осталось дней: {}".format(quest_days_left))
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
		
	level_date = level_schedule[level]
	level_delta = level_date - today
	level_days_left = level_delta.days
	if level_days_left > 0:
		await bot.say(level_date.strftime("%d.%m") + ", осталось дней: {}".format(level_days_left))
	else:
		await bot.say(level_date.strftime("%d.%m"))
	
@bot.command()
async def vote(sought_quest: str, *args):
	if sought_quest.find("чел") + 1:
		sought_quest = "челлендж"
	
	quests = set(map(lambda quest: quest["name"], vote_schedule))
	if sought_quest not in quests:
		await bot.say("Таких квестов не знаю")
		return
			
	rating = None
	if args:
		if args[0] not in ["рейтинг", "нерейтинг"]:
			await bot.say("Квест либо рейтинговый, либо нерейтинговый, третьего не дано")
			return
		else:
			rating = True if args[0] == "рейтинг" else False

	# фильтруем список голосования
	if rating is None: # оставляем квесты без разделения на рейтинг и нерейтинг
		vote_schedule_filtered = list(filter(lambda quest: "rating" not in quest.keys(), vote_schedule))
	elif rating: # оставляем рейтинговые
		vote_schedule_filtered = list(filter(lambda quest: "rating" in quest.keys() and quest["rating"], vote_schedule))
	else: # оставляем нерейтинговые
		vote_schedule_filtered = list(filter(lambda quest: "rating" in quest.keys() and not quest["rating"], vote_schedule))
			
	quests = set(map(lambda quest: quest["name"], vote_schedule_filtered))
	if sought_quest not in quests:
		await bot.say("У этого квеста нет разделения на рейтинг и нерейтинг")
		return 
	
	for quest in vote_schedule_filtered:
		if sought_quest == quest["name"]: # название искомого квеста встретилось в списке
			if quest["beginning"] > today: # если дата начала голосования позже сегодня
				await bot.say("Голосование за {} ещё не началось".format(quest["out"]))
				break
			elif quest["end"] < today: # если дата окончания голосования раньше сегодня
				await bot.say("Голосование за {} уже закончилось".format(quest["out"]))
				break
			else:			
				await bot.say("Голосование за {} закончится ".format(quest["out"]) + quest["end"].strftime("%d.%m"))
				break
	
@bot.command()
async def help_():
    embed = discord.Embed(title="fandom-kombat-schedule", description="Расписание ФБ. Бот принимает команду и одно слово/цифру. **Команды:**", color=0xeee657)

    embed.add_field(name="$schedule", value="Выводит картинку с расписанием", inline=False)
    embed.add_field(name="$quest %X%", value="Выводит даты выкладок для квеста под названием **X** и оставшееся количество дней до начала, если он в будущем", inline=False)
    embed.add_field(name="$level %X%", value="Выводит дату начала левела номер **X** и оставшееся количество дней, если он в будущем", inline=False)
    embed.add_field(name="$bonus", value="Выводит даты выкладки бонуса", inline=False)
    embed.add_field(name="$non_comp", value="Выводит даты выкладки внеконкурса", inline=False)
    embed.add_field(name="$deadline", value="Подбадривает", inline=False)
    embed.add_field(name="$vote %X% [рейтинг/нерейтинг]", value="Сколько осталось до конца голосования за квест **X**, рейтинговый или нет", inline=False)
    embed.add_field(name="$help_", value="Выводит эту справку", inline=False)
    await bot.say(embed=embed)

bot.run(conf.token)
