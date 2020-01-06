import uuid
from datetime import datetime
from datetime import time
#from django.test import TestCase
from .models import Meeting

# Create your tests here.


def genTestData():
    now = datetime.now()

    for item in range(10):
        mname = '测试答辩课题_{}'.format(item)
        delta = datetime.timedelta(days=time)
        n_days = now + delta
        time.strftime("%Y-%m-%d %H:%M:%S", n_days) 
        Meeting(pid=uuid.uuid4,
                m_name=mname,
                m_date='2020-01-01',
                m_stime=time(10, 00, 00),
                m_etime=time(10, 10, 00),
                m_inteval=10,
                m_mp='张三',
                m_mobile='0000').save()


if __name__ == '__main__':
    genTestData()
    pass
