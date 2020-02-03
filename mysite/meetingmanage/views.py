#from django.shortcuts import render
import xlrd
import uuid

from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Meeting
from . import tests

# Create your views here.


def gendata(request):
    tests.genTestData()
    #FIXME url 硬编码
    return redirect(reverse("index"))


def cleardata(request):
    tests.cleardata()
    return redirect(reverse("index"))


def delmeetings(request, pid):
    meeting = get_object_or_404(Meeting, pk=int(id))
    meeting.delete()
    return redirect(reverse("index"))


def delmeeting(request):

    if (request.method == 'POST'):
        print("the POST method")
        concat = request.POST
        postBody = request.body
        pids = concat['selectedPid']
        print('pids {}'.format(pids))
        if (pids):
            Meeting.objects.extra(where=['pid IN (' + pids + ')']).delete()
            messages.success(request, '已删除', extra_tags='alert-success')
    return redirect(reverse("index"))


def index(request):

    meetinglist = Meeting.objects.order_by('-m_date', '-m_stime',
                                           'createtime')  # 答辩日期 答辩开始时间降序排序
    #FIXME  url 硬编码
    template = loader.get_template('meetingmanage/index.html')
    tc_json = ''
    for meeting in meetinglist:
        # print(meeting)
        #FIXME 答辩时间格式化抽取到工具方法中
        tc_json = tc_json + '{' + 'pid: "{}", m_guide: "{}", m_room: "{}", m_name: "{}", m_date: "{}", m_time: "{}", m_inteval: "{}", m_mp: "{}", m_mobile: "{}",  createtime: "{}"'.format(
            meeting.pid, meeting.m_guide, meeting.m_room, meeting.m_name,
            meeting.m_date, (meeting.m_stime.strftime("%H:%M") + " - " +
                             meeting.m_etime.strftime("%H:%M")),
            meeting.m_inteval, meeting.m_mp, meeting.m_mobile,
            meeting.createtime.strftime('%Y-%m-%d %H:%M')) + '}'
        tc_json = tc_json + ','
    tc_json = '[{}]'.format(tc_json)
    context = {
        'tc_json': tc_json,
        #'meetinglist': meetinglist
    }
    #return render_to_response('meetingmanage/index.html', context) 3.0 移除该方法
    return HttpResponse(template.render(context, request))


def test(request):
    #FIXME template url hardcode
    template = loader.get_template('meetingmanage/testzui.htm')
    context = {}

    return HttpResponse(template.render(context, request))


def importExcel(request):
    if "GET" == request.method:
        return redirect("/meetingmanage/")
    elif "POST" == request.method:
        try:
            excel_file = request.FILES['importExcel']
            wb = xlrd.open_workbook(filename=None,
                                    file_contents=excel_file.read())
            table = wb.sheets()[0]
            total_rows = table.nrows  # 拿到总共行数
            now = datetime.now()
            for rowindex in range(1, total_rows):  # 跳过首行标题
                row = table.row_values(rowindex)

                timestr = row[2]
                stime = None
                etime = None

                interval = 0
                #FIXME 答辩时间解析, 间隔计算抽取到工具方法中
                if timestr.strip() != '':
                    timearray = timestr.split('-')
                    stime = datetime.strptime(timearray[0].strip(), "%H:%M")
                    etime = datetime.strptime(timearray[1].strip(), "%H:%M")
                    interval = (etime - stime).seconds / 60

                # 0答辩地点    1答辩日期    2答辩时间    3所属专项    4项目编号    5项目名称    6项目负责人    7联系方式    8申报单位    9推荐单位
                # print(row)
                pidstr = uuid.uuid4()
                Meeting(
                    pid=pidstr,
                    m_room=row[0],
                    m_date=row[1],
                    m_guide=row[3],
                    m_number=row[4],
                    m_name=row[5],
                    m_mp=row[6],
                    m_mobile=row[7],
                    m_org=row[8],
                    m_orgre=row[9],
                    createtime=now,
                    m_stime=stime,
                    m_etime=etime,
                    m_inteval=interval,
                ).save()

            wb.release_resources()
        except BaseException as e:
            print(e.message)
            return HttpResponse('fail')
        finally:
            del wb
    return redirect(reverse("index"))