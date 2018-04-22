import asyncio
import discord
import json
from discord.ext import commands
from functions import (last_news, edit_message,
						get_last_date, save_last_date,
						get_dk_names,add_member)
from models import Date

token     = token
channel   = discord.Object(id=id)
server_id = id
bot       = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

@bot.command(pass_context=True)
async def add(ctx, vk_name:str, dk_name:str):
	if add_member(vk_name,dk_name):
		await bot.say('added')
	else:
		await bot.say('Error!')
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