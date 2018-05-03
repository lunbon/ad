import sys
import requests, re
import json
import discord
from bs4 import BeautifulSoup as bs4
from models import Date

url='https://vk.com/angeldevmanga'
'''functions for parsing vk'''
def get_last_posts(last_date=None):
	posts=[]
	response=requests.get(url)
	if response.status_code!=200:
		raise "Error "+status_code
	html  = response.text
	soup  = bs4(html,'html.parser')
	for item in soup.find_all('a', class_='wi_date'):
		post_href = '?w='+item.get('href')[1:]
		post = bs4(requests.get(url+post_href).text,'html.parser')
		if last_date is None:
			return [post]
		date=get_date(post)
		if date<last_date:break
		else:posts.append(post)
	return posts

def get_language(post):
	text=re.findall("Переведено с .*",str(post))[0].split('<br/>')[0]
	return bs4(text,'html.parser').get_text()
def get_vk_names(post):
	text=re.findall("Над главой работали: .*",str(post))[0].split('<br/>')[0][21:-1]
	return bs4(text,'html.parser').get_text().split(', ')

def get_dk_names(translators,server,team):
	dk_names=[]
	members = team.get_all_members()
	for name in translators:
		if name in members.keys():
			dk_names.append(server.get_member(members[name]).mention)
		else:
			if name[0]=='#':name=name[1:]
			dk_names.append(name)
	return dk_names

def get_links(post):
	links = post.find_all('a')
	new_links = []
	for i in range(len(links)):
		if links[i].get_text().startswith('http'):
			new_links.append(links[i-1].get_text()[1:]+': '+links[i].get_text())
	return new_links

def get_title(post):
	return re.findall('<div class="pi_text">[^<]*',str(post))[0][21:]

def get_date(post):
	return Date(post.find_all('span', class_='wi_date')[0].text)

def get_last_date():
	if len(sys.argv) == 1:date = get_date(get_last_posts()[0])
	else: date = Date(sys.argv[1])
	return date

def last_news(last):
	posts = get_last_posts(last)
	titles=[]
	for post in posts:
		date  =       get_date(post)
		title =       get_title(post)
		links =       get_links(post)
		translators = get_vk_names(post)
		language = get_language(post)
		titles.append({
					'date':date,
					'title':title,
					'links':links,
					'translators':translators,
					'language':language
					})
	return titles
'''functions for editing raw data'''
def edit_links(links):
	return '\n'.join(links)

def edit_translators(translators):
	return ', '.join(translators)

def get_embed(title,translators,links,language, bot):
	'''The function return embeded message'''
	fields = []
	for link in links:
		fields.append({
			'name':link.split(':')[0],
			'value': '[тык]('+link.split(': ')[1]+')',
			'inline':True
			})

	translators = edit_translators(translators)
	description = ("*Над переводом работали: "+translators+'*')
	embed = {
			"description":description,
			"colour":0x00bfff}
	embed = discord.Embed(**embed)
	embed.set_author(name=title,icon_url=bot.user.default_avatar_url)
	for field in fields:embed.add_field(**field)
	embed.set_footer(text=language,icon_url='https://images-ext-2.discordapp.net/external/bQOHBE_ApJFlLTeOUYdZBC-KhPKacnCoBQKXFp4PYzE/https/pp.userapi.com/c638721/v638721291/6ead8/PkwxZ165LXA.jpg')
	return embed
