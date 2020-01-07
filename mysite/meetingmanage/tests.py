import uuid
import datetime
#from django.test import TestCase
from .models import Meeting

# Create your tests here.


def genTestData():
    now = datetime.datetime.now()

    for item in range(10):
        mname = '测试答辩课题_{}'.format(item)
        delta = datetime.timedelta(days=item)
        n_days = now + delta
        n_daystr = n_days.strftime('%Y-%m-%d')  #datetime.time.strftime('%Y-%m-%d')
        pidstr = uuid.uuid4()
        Meeting(pid=pidstr,
                m_name=mname,
                m_date=n_daystr,
                m_stime=datetime.time(10, 00, 00),
                m_etime=datetime.time(10, 10, 00),
                m_inteval=10,
                m_mp='张三',
                m_mobile='0000').save()


if __name__ == '__main__':
    genTestData()
    pass
