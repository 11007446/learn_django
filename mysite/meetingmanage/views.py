#from django.shortcuts import render
import xlrd
import uuid

from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
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

        concat = request.POST
        postBody = request.body
        pids = concat['selectedPid']
        if (pids):
            Meeting.objects.filter(pid__in=pids.split(',')).delete()
            messages.success(request,
                             "项目 " + concat['selectedPname'] + ' 视频答辩记录 删除成功',
                             extra_tags='alert-success')
    return redirect(reverse("index"))


def showmeeting(request):
    # 模态窗口 返回json
    if (request.method == 'POST'):
        concat = request.POST
        selectedPid = concat['editPid']
        if (selectedPid):
            meeting = Meeting.objects.get(pid=selectedPid)
            meetingjson = '{' + '"pid": "{}", "m_guide": "{}", "m_room": "{}", "m_name": "{}", "m_date": "{}", "m_stime": "{}", "m_etime": "{}", "m_inteval": "{}", "m_mp": "{}", "m_mobile": "{}", "m_org": "{}", "m_orgre": "{}"'.format(
                meeting.pid, meeting.m_guide, meeting.m_room, meeting.m_name,
                meeting.m_date, meeting.m_stime.strftime("%H:%M"),
                meeting.m_etime.strftime("%H:%M"), meeting.m_inteval,
                meeting.m_mp, meeting.m_mobile, meeting.m_org,
                meeting.m_orgre) + '}'
        return HttpResponse(meetingjson)
    else:
        return redirect(reverse("index"))


def preparQ(q, con_name, con_value, con_suf='', func_format=None):
    """将查询条件填充Q查询对象
    Arguments:
        q {[type]} -- [Q查询对象]
        con_suf {[type]} -- [查询条件后缀 例: __contains __glt ] (default: "")
        con_name {[type]} -- [查询参数名称]
        con_value {[type]} -- [查询参数值]
    Keyword Arguments:
        func_format {[type]} -- [格式化参数值回调函数] (default: {None})
    Returns:
        [type] -- [返回填充后的Q对象]
    """
    if (con_value):  # 参数值非空,该查询条件起效
        if (func_format):  # 提供参数格式化函数,对参数进行格式化
            q.children.append((con_name + con_suf, func_format(con_value)))
        else:
            q.children.append((con_name + con_suf, con_value))
    return q


def index(request):
    #FIXME  url 硬编码
    template = loader.get_template('meetingmanage/index.htm')
    tc_json = ''
    meetinglist = None
    # POST 点击查询按钮
    if "POST" == request.method:
        #FIXME 使用FORM来更优雅的处理查询字段
        concat = request.POST
        m_room_s = concat['m_room_s']
        m_name_s = concat['m_name_s']
        m_guide_s = concat['m_guide_s']
        m_mp_s = concat['m_mp_s']
        m_date1 = concat['m_date1']
        m_date2 = concat['m_date2']
        createtime1 = concat['createtime1']
        createtime2 = concat['createtime2']

        #con_dict = {}  # 条件字典
        #fillconditiondict(con_dict, '')
        # Q使用案例 OR: list.filter(Q(pk_ _lt=6) | Q(bcommet_ _gt=10))
        # Q使用案例 AND: list.filter(Q(pk_ _lt=6) & Q(bcommet_ _gt=10))

        q1 = Q()
        q1.connector = 'AND'
        # 精确查询
        preparQ(q1, 'm_room', m_room_s)
        # 模糊查询
        preparQ(q1, 'm_name', m_name_s, con_suf='__contains')
        preparQ(q1, 'm_guide', m_guide_s, con_suf='__contains')
        preparQ(q1, 'm_mp', m_mp_s, con_suf='__contains')
        # 范围查询
        preparQ(q1, 'm_date', m_date1, con_suf='__gte')
        preparQ(q1, 'm_date', m_date2, con_suf='__lte')

        # q1.children.append(('m_name__contains', m_name_s))
        # q1.children.append(('m_guide__contains', m_guide_s))
        # q1.children.append(('m_mp__contains', m_mp_s))
        # 范围查询
        # q1.children.append(('m_name__contains', m_name_s))

        meetinglist = Meeting.objects.filter(q1).order_by(
            '-m_date', '-m_stime', 'createtime')
    else:
        pass
        meetinglist = Meeting.objects.order_by('-m_date', '-m_stime',
                                               'createtime')  # 答辩日期 答辩开始时间降序排序
    array_json = []
    for meeting in meetinglist:
        # print(meeting)
        #FIXME 答辩时间格式化抽取到工具方法中
        array_json.append(
            '{' +
            'pid: "{}", m_guide: "{}", m_lotno: "{}", m_room: "{}", m_name: "{}", m_date: "{}", m_time: "{}", m_inteval: "{}", m_mp: "{}", m_mobile: "{}",  createtime: "{}"'
            .format(meeting.pid, meeting.m_guide, meeting.m_lotno,
                    meeting.m_room, meeting.m_name, meeting.m_date,
                    (meeting.m_stime.strftime("%H:%M") + " - " +
                     meeting.m_etime.strftime("%H:%M")
                     ), meeting.m_inteval, meeting.m_mp, meeting.m_mobile,
                    meeting.createtime.strftime('%Y-%m-%d %H:%M')) + '}')
    tc_json = ','.join(array_json)
    tc_json = '[{}]'.format(tc_json)

    context = {
        'tc_json': tc_json,
        #'meetinglist': meetinglist
    }
    return HttpResponse(template.render(context, request))


def test(request):
    #FIXME template url hardcode
    template = loader.get_template('meetingmanage/testzui.htm')
    context = {}

    return HttpResponse(template.render(context, request))


def formatmdate(mdatestr):
    """[格式化日期函数]
    预留该函数应对日后各种日期格式的情况
    目前只针对 XXXX年XX月XX日 格式
    Arguments:
        mdatestr {[字符串]} -- [description]
    Returns:
        [datetime] -- [description]
    """
    formatresult = datetime.strptime(mdatestr, '%Y年%m月%d日')
    return formatresult



def submitedit(request):
    if "POST" == request.method:
        concat = request.POST
        editPid = concat['editPid']
        meeting = Meeting.objects.get(pid=editPid)
        m_stime = concat['m_stime']
        m_etime = concat['m_etime']
        stime = datetime.strptime(m_stime.strip(), "%H:%M")
        etime = datetime.strptime(m_etime.strip(), "%H:%M")
        count_inteval = (etime - stime).seconds / 60
        meeting.m_room = concat['m_room']
        meeting.m_date = concat['m_date']
        meeting.m_guide = concat['m_guide']
        meeting.m_name = concat['m_name']
        meeting.m_mp = concat['m_mp']
        meeting.m_mobile = concat['m_mobile']
        meeting.m_stime = m_stime
        meeting.m_etime = m_etime
        meeting.m_inteval = count_inteval
        meeting.m_org = concat['m_org']
        meeting.m_orgre = concat['m_orgre']
        meeting.save()
    return redirect(reverse("index"))


def importExcel(request):
    if "GET" == request.method:
        return redirect("/meetingmanage/")
    elif "POST" == request.method:
        try:
            concat = request.POST
            m_lotno = concat['m_lotno']
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
                    m_lotno=m_lotno,
                    m_room=row[0],
                    m_date=formatmdate(row[1]),
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
