import uuid
import datetime
import random
#from django.test import TestCase
from .models import Meeting

# Create your tests here.


# 返回指定位数随机数
def randomNunStr(numsize):
    numlist = []
    for number in range(numsize):
        str2 = str(random.randint(0, 9))
        numlist.append(str2)
    numstr = " ".join(numlist).replace(" ", "")
    return numstr


def cleardata():
    Meeting.objects.all().delete()  # 删除全部数据


def genTestData():
    now = datetime.datetime.now()
    #TODO 测试数据清理
    Meeting.objects.all().delete()  # 删除全部数据

    # 插入测试数据
    ctime = datetime.datetime.now()
    for item in range(50):
        mname = '测试答辩课题_{}'.format(item)
        delta = datetime.timedelta(days=item)
        n_days = now + delta
        n_daystr = n_days.strftime(
            '%Y-%m-%d')  #datetime.time.strftime('%Y-%m-%d')
        pidstr = uuid.uuid4()
        Meeting(pid=pidstr,
                m_name=mname,
                m_date=n_daystr,
                m_stime=datetime.time(10, 00, 00),
                m_etime=datetime.time(10, 10, 00),
                m_inteval=10,
                m_mp='张三',
                m_org='承担单位',
                m_orgre='推荐单位',
                createtime=ctime,
                m_guide='项目指南',
                m_mobile='1' + randomNunStr(10)).save()


if __name__ == '__main__':
    genTestData()
    pass
