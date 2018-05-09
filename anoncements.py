import asyncio
import discord
import json
from discord.ext import commands
from functions import last_news, get_embed, \
						get_last_date,get_dk_names
from models import Date, Team

token     = token
channel   = discord.Object(id='407369776625614848')
role_id   = '404996151121543169'
bot       = commands.Bot(command_prefix='?')
server_id = '404992131539795968'
team = Team('team.json')

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

@bot.command(pass_context=True)
async def add(ctx, vk_name:str, dk_name:str):
	server=bot.get_server(server_id)
	member = ctx.message.author
	role = list(filter((lambda x:x.id==role_id),member.roles)) 
	if role!=[]:
		if team.add_member(vk_name,dk_name):
			await bot.say('added')
		else:
			await bot.say('Error!')
	else:
		await bot.say('Нет прав!')
@bot.command
async def show():
	members = team.all_members
	for key in members:
		message+='%s - %s'%(key,member[key])
	bot.say(message)
@bot.command()
async def last():
	server=bot.get_server(server_id)
	post  = last_news()[0]
	dk_names = get_dk_names(post['translators'],server,team)
	embed    = get_embed(post['title'],dk_names,
				post['links'],post['language'],bot)
	await bot.say(embed=embed)

async def check_anoncements():
	await bot.wait_until_ready()
	date   = get_last_date()
	server=bot.get_server(server_id)
	while not bot.is_closed:
		posts = last_news(date)
		for post in posts:
			dk_names = get_dk_names(post['translators'],server,team)
			embed    = get_embed(post['title'],dk_names,
								post['links'],post['language'],bot)
			await bot.send_message(channel, embed=embed)
			date = post['date']
		await asyncio.sleep(1000)

bot.loop.create_task(check_anoncements())
bot.run(token)