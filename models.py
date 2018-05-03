from datetime import datetime
import json
class Date:
	def __init__(self,date):
		'''Дата вида "1 апр в 3:48"'''
		self.table={
				'янв':1,
				'фев':2,
				'мар':3,
				'апр':4,
				'май':5,
				'июн':6,
				'июл':7,
				'авг':8,
				'сен':9,
				'окт':10,
				'ноя':11,
				'дек':12}
		day = date[:2].strip()
		if day == 'вч' or day == 'се':
			now = datetime.now()
			self.month = now.month
			minutes = date[-2:]
			if minutes[0]==':':
				minutes=minutes[1:]
				date=date[:-4]
			else:date=date[:-3]
			self.minutes = int(minutes)
			self.hour = date[-2:].strip()
			if day == 'се':self.day = now.day
			else:self.day = now.day-1
		else:
			self.month=self.table[date[2:6].strip()]
			self.day=int(day)
			self.minutes=int(date[-2:])
			self.hour=int(date[-5:-3].strip())

	def __eq__(self,other):
		return (True if (self.month==other.month and
						self.day==other.day and
						self.hour==other.hour and
						self.minutes==other.minutes) else False)

	def __lt__(self, other):
		if self.month!=other.month:
			return False if self.month>other.month else True
		if self.day!=other.day:
			return False if self.day>other.day else True
		if self.hour!=other.hour:
			return False if self.hour>other.hour else True
		return False if self.minutes>other.minutes else True

	def __le__(self,other):
		return self<other or self==other

class Team:
	def __init__(self,filename='team.json'):
		try:
			file=open(filename,'r')
			json.loads(f.read())
			file.close()
		except:
			file=open(filename,'w')
			file.write('{"Sawich": "206789210009632768",'+ 
						'"TheDarkLord": "391977557886500874"}')
			file.close()
		self.filename = filename
	def get_all_members(self):
		try:
			with open(self.filename,'r') as f:
				members = json.loads(f.read())
			return members
		except:
			return {}
	def add_member(self,vk_name,dk_name):
		new_member={vk_name:dk_name}
		with open(self.filename,'r') as f:
			old_members=json.loads(f.read())
		try:
			with open(self.filename,'w') as f:
				f.write(str(json.dumps({**old_members,**new_member})))
				return True
		except:
			with open(self.filename,'w') as f:
				f.write(str(json.dumps(old_members)))
				return False
