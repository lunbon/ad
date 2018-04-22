import sys
import requests, re
import json
import discord
from bs4 import BeautifulSoup as bs4
from models import Date


url='https://vk.com/angeldevmanga'

def get_last_posts(last_date):
	posts=[]
	response=requests.get(url)
	if response.status_code!=200:
		raise "Error "+status_code
	html  = response.text
	soup  = bs4(html,'html.parser')
	for item in soup.find_all('a', class_='wi_date'):
		post_href = '?w='+item.get('href')[1:]
		post = bs4(requests.get(url+post_href).text,'html.parser')
		date=get_date(post)
		if date<last_date:break
		else:posts.append(post)
	return posts

def get_vk_names(post):
	text=re.findall("Над главой работали: .*",str(post))[0].split('<br/>')[0][21:-1]
	return bs4(text,'html.parser').get_text().split(', ')

def get_dk_names(translators,server):
	dk_names=[]
	with open('team.json','r') as f:
		names=json.loads(f.read())
	for name in translators:
		if name in names.keys():
			dk_names.append(server.get_member(names[name]).mention)
		else:
			if name[0]=='#':name=name[1:]
			dk_names.append(name)
	return dk_names

def get_links(post):
	links = post.find_all('a')
	new_links = []
	for i in range(len(links)):
		if links[i].get_text().startswith('http'):
			new_links.append(links[i-1].get_text()+': '+links[i].get_text())
	return new_links

def get_title(post):
	return re.findall('<div class="pi_text">[^<]*',str(post))[0][21:]

def get_date(post):
	return Date(post.find_all('span', class_='wi_date')[0].text)

def last_news(last):
	posts = get_last_posts(last)
	titles=[]
	for post in posts:
		date  =       get_date(post)
		title =       get_title(post)
		links =       get_links(post)
		translators = get_vk_names(post)
		titles.append({
					'date':date,
					'title':title,
					'links':links,
					'translators':translators
					})
	return titles

def edit_links(links):
	return '\n'.join(links)

def edit_translators(translators):
	return ', '.join(translators)

def edit_message(title,translators,links):
	links       = edit_links(links)
	translators = edit_translators(translators)
	description = ("Над переводом работали: "+translators+
					"\n\n"+links+'\n\n')
	embed = {"title":title,'description':description,
			"colour":0x00bfff}
	return embed

def get_last_date():
	if len(sys.argv) == 1:date = Date('7 мар в 11:46')
	else: date = Date(sys.argv[1])
	return date

def save_last_date(date):
	return 0
def add_member(vk_name,dk_name):
	new_member={vk_name:dk_name}
	with open('team.json','r') as f:
		old_members=json.loads(f.read())
	try:
		with open('team.json','w') as f:
			f.write(str(json.dumps({**old_members,**new_member})))
			return True
	except:
		with open('team.json','w') as f:
			f.write(str(json.dumps(old_members)))
			return False