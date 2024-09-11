import datetime
import re
months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Avg':'08','Sep':'09','Oct':'10','Nov':'11','Dec': '12'}
zd = 'Wed, 11 Sep 2024 07:15:30 +0300'
s = ', '
p = re.search('(?<=' + s + ').*?(?= )', zd)
d = p.group(0)
s = s+d+' '
p = re.search('(?<=' + s + ').*?(?= )', zd)
m0 = p.group(0)
s = s +m0+' '
m = months[m0]
p = re.search('(?<=' + s + ').*?(?= )', zd)
y = p.group(0)
s =s +y+' '
p = re.search('(?<=' + s + ').*?(?=:)', zd)
cl = p.group(0)
s=s+cl+':'
p = re.search('(?<=' + s + ').*?(?=:)', zd)
mn = p.group(0)
s=s+mn+':'
p = re.search('(?<=' + s + ').*?(?= )', zd)
sc = p.group(0)
z = zd.split(' ')[5]
print(d,m,y,cl,mn,sc,z)

now_date = datetime.datetime.now()
#print(datetime.datetime.astimezone())
print(now_date)

some_date = datetime.datetime(int(y), int(m), int(d),int(cl),int(mn),int(sc))
#+ timedelta(hours=3)
print(some_date)
a = some_date - now_date
print(a.seconds)