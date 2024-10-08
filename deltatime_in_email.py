import datetime
import re
months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Avg':'08','Sep':'09','Oct':'10','Nov':'11','Dec': '12'}
def deltatime_in_email(zd,now_zone):
    # где zd дата в формате 'Wed, 11 Sep 2024 14:28:30 +0300'
    # now_zone - зона времени по которой получаем текущую дату и время now()
    # возвращает разницу zd и текущей даты времени в секундах
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
    #print(d,m,y,cl,mn,sc,z)

    now_date = datetime.datetime.now()
    #print(datetime.datetime.astimezone())
    #print(now_date)

    now_date = now_date - datetime.timedelta(hours=now_zone)

    some_date = datetime.datetime(int(y), int(m), int(d),int(cl),int(mn),int(sc))
    #print(some_date)
    some_date= some_date-datetime.timedelta(hours=int(z)/100)
    #print('z',some_date)
    #print('z',now_date)
    a = now_date - some_date
    return a.seconds
if __name__=='__main__':
    zd = 'Wed, 11 Sep 2024 14:28:30 +0300'
    print(deltatime_in_email(zd,5))