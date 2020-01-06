#from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Meeting
from . import tests
# Create your views here.


def gendata(request):
    #TODO 生成失败增加500提示
    tests.genTestData()
    return HttpResponse('测试数据生成成功')


def index(request):
    #TODO 查询前10答辩数据回传
    meetinglist = Meeting.objects.order_by('-m_date',
                                           '-m_stime')  # 答辩日期 答辩开始时间降序排序
    template = loader.get_template('meetingmanage/index.html')
    context = {
        'meetinglist': meetinglist,
    }
    return HttpResponse(template.render(context, request))
