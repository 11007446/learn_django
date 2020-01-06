from django.db import models

# Create your models here.


class Meeting(models.Model):
    S1 = 'S1'
    S2 = 'S2'
    M_ROOM = {
        (S1, '上海1'),
        (S2, '上海2'),
    }
    pid = models.CharField(max_length=50, primary_key=True)

    m_room = models.CharField(  # 答辩室
        max_length=100,
        choices=M_ROOM,
        # default=S1,
    )

    m_name = models.CharField(max_length=100)  # 答辩项目名称

    m_date = models.CharField(max_length=10)  # 答辩日期

    m_stime = models.TimeField()  # 答辩时间起

    m_etime = models.TimeField()  # 答辩时间止

    m_inteval = models.IntegerField()  # 答辩时长

    m_mp = models.CharField(max_length=50)  # 答辩人

    m_mobile = models.CharField(max_length=20)  # 答辩人联系方式
