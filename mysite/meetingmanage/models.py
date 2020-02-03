from django.db import models

# Create your models here.


class Meeting(models.Model):

    pid = models.CharField(max_length=50, primary_key=True)

    m_room = models.CharField(max_length=10, default='上海1')  # 答辩室

    m_name = models.CharField(max_length=100)  # 答辩项目名称

    m_date = models.CharField(max_length=10)  # 答辩日期

    m_stime = models.TimeField()  # 答辩时间起

    m_etime = models.TimeField()  # 答辩时间止

    #createtime = models.TimeField()  # 答辩记录创建时间
    createtime = models.DateTimeField()  # 答辩记录创建时间 timefield只记录时分秒 DateTimeField 时分秒年月日

    m_inteval = models.IntegerField()  # 答辩时长

    m_mp = models.CharField(max_length=50, default='')  # 答辩人

    m_mobile = models.CharField(max_length=20, default='')  # 答辩人联系方式

    m_guide = models.CharField(max_length=300, default='')  # 答辩项目指南

    m_org = models.CharField(max_length=100, default='')  # 项目承担单位

    m_orgre = models.CharField(max_length=100, default='')  # 项目推荐单位
    m_number = models.CharField(max_length=50, default='')  # 项目编号







