import discord
import conf
from discord.ext import commands
from datetime import date

bot = commands.Bot(command_prefix='$', description='A bot that gives FK schedule')

today = date.today()
quest_schedule = {'визитка': [date(today.year, 7, 21), date(today.year, 7, 22)],
			'челленж': [date(today.year, 8, 15), date(today.year, 8, 16)],
			'челлендж': [date(today.year, 8, 15), date(today.year, 8, 16)],
			'бб': [date(today.year, 8, 26), date(today.year, 8, 27)],
			'спецквест': [date(today.year, 9, 26), date(today.year, 9, 27)]}

level_schedule = {1: date(today.year, 7, 21),
            2: date(today.year, 7, 26),
            3: date(today.year, 8, 15),
            4: date(today.year, 8, 26),
            5: date(today.year, 9, 6),
            6: date(today.year, 9, 26)}			
			
vote_schedule = {}
			
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)

@bot.command()
async def deadline():
    await bot.say("Похуй, пляшем :dancer: :man_dancing:")
	
@bot.command()
async def schedule():
    schedule = discord.Embed()
    schedule.set_image(url="http://funkyimg.com/i/2DVSq.png")
    await bot.say(embed=schedule)

@bot.command()
async def quest(quest: str):
	quest_first_date = quest_schedule[quest.lower()][0]
	quest_second_date = quest_schedule[quest.lower()][1]
	quest_delta = quest_first_date - today
	quest_days_left = quest_delta.days
	if quest_days_left > 0:
		await bot.say(quest_first_date.strftime("%d.%m") + '-' + quest_second_date.strftime("%d.%m") + ', осталось дней: {}'.format(quest_days_left))
	else:
		await bot.say(quest_first_date.strftime("%d.%m"))
	
@bot.command()
async def level(level):
	if type(level) is not int:
		await bot.say("Таких левелов не знаю")
	elif level not in range(1, 7):
		await bot.say("Таких левелов не знаю")
	else:
		level_date = level_schedule[level]
		level_delta = level_date - today
		level_days_left = level_delta.days
		if level_days_left > 0:
			await bot.say(level_date.strftime("%d.%m") + ', осталось дней: {}'.format(level_days_left))
		else:
			await bot.say(level_date.strftime("%d.%m"))
	
@bot.command()
async def vote(quest: str, *args):
	# if not args:
		
	# if args:
		# level = args[0]
	await bot.say(quest)
	
@bot.command()
async def help_():
    embed = discord.Embed(title="fandom-kombat-schedule", description="Расписание ФБ. Бот принимает команду и одно слово/цифру. **Команды:**", color=0xeee657)

    embed.add_field(name="$schedule", value="Выводит картинку с расписанием", inline=False)
    embed.add_field(name="$quest X", value="Выводит даты выкладок для квеста под названием **X** и оставшееся количество дней до первого, если он в будущем", inline=False)
    embed.add_field(name="$level X", value="Выводит дату начала левела номер **X** и оставшееся количество дней, если он в будущем", inline=False)
    embed.add_field(name="$deadline", value="Подбадривает", inline=False)
    embed.add_field(name="$vote ...", value="Сколько осталось до конца голосования за ...", inline=False)
    embed.add_field(name="$help_", value="Выводит эту справку", inline=False)
    await bot.say(embed=embed)

bot.run(conf.token)
