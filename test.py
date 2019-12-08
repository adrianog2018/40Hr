import datetime

today = datetime.date.today()
# today = datetime.date(2019,12,9)
last_sunday = today - datetime.timedelta(days=today.weekday())
coming_saturday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
# print(today)
idx = (today.weekday()+1) % 7 # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
# print(idx)
sun = today - datetime.timedelta(idx)
mon = today - datetime.timedelta(idx-1)
tue = today - datetime.timedelta(idx-2)
wed = today - datetime.timedelta(idx-3)
thu = today - datetime.timedelta(idx-4)
fri = today - datetime.timedelta(idx-5)
sat = today - datetime.timedelta(idx-6)
# print(sun) 
# print(mon)   
# print(tue) 