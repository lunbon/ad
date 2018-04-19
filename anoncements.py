import asyncio
import discord
import json
from discord.ext import commands
from functions import (last_news, edit_message,
						get_last_date, save_last_date,
						get_dk_names)
from models import Date

token     = 'token'
channel   = discord.Object(id='417269196850987029')
server_id = 'server_id'
bot       = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

async def check_anoncements():
	await bot.wait_until_ready()
	date  = get_last_date()
	server = bot.get_server(server_id)
	while not bot.is_closed:
		posts = last_news(date)
		for post in posts:
			dk_names=get_dk_names(post['translators'],server)
			message = edit_message(post['title'],dk_names,
								post['links'])
			embed = discord.Embed(**message)
   
			await bot.send_message(channel,embed=embed)
			date = post['date']
		await asyncio.sleep(3600)

bot.loop.create_task(check_anoncements())
bot.run(token)