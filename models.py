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
		self.day=int(date[:2].strip())
		self.month=self.table[date[2:6].strip()]
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
		