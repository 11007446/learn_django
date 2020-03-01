import traceback
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import datetime

from datetime import timedelta

host_server = 'smtp.qq.com'
sender = '11007446@qq.com'
pwd = 'gfhzbxxdlczecahh'  # 此处填写qq邮箱的授权码
sender_mail = '11007446@qq.com'
receivers = ['cjl@shkeshen.com']


def getweekdayinfo():
    today = datetime.datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = today + timedelta(days=6 - today.weekday())
    weekdayinfo = "({} - {})".format(monday.strftime("%Y-%m-%d"),
                                     sunday.strftime("%Y-%m-%d"))
    return weekdayinfo


def getweekdayrange():
    weekdayrange = []
    today = datetime.datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = today + timedelta(days=6 - today.weekday())
    weekdayrange.append(monday.strftime("%Y-%m-%d"))
    weekdayrange.append(sunday.strftime("%Y-%m-%d"))
    return weekdayrange


def sendweekplanmail(meetings):
    mail_content = """
        <br>
        <div>本周视频答辩安排如下:{}</div>
        <br>
        <div>
            <font color='#ff0000'>本周安排中有异常情况，请运维人员注意！</font>
        </div>
        <br>

        <table border='1' bordercolor='#000000' cellpadding='2' cellspacing='0'
            style='font-size: 10pt; border-collapse:collapse;' width='50%'>
            <tbody>
                <tr>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div><span
                                    class='celltext'>序号</span>&nbsp;
                            </div>
                        </font>
                    </td>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div>&nbsp;<span
                                    class='celltext'>项目名称</span>
                            </div>
                        </font>
                    </td>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div>&nbsp;<span
                                    class='celltext'>所属指南</span>
                            </div>
                        </font>
                    </td>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div>&nbsp;<span
                                    class='celltext'>答辩日期</span>
                            </div>
                        </font>
                    </td>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div>&nbsp;<span
                                    class='celltext'>答辩时间</span>
                            </div>
                        </font>
                    </td>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div>&nbsp;<span
                                    class='celltext'>负责人</span>
                            </div>
                        </font>
                    </td>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div>&nbsp;<span
                                    class='celltext'>联系电话</span>
                            </div>
                        </font>
                    </td>
                    <td width='12%' nowrap=''>
                        <font size='2' face='Verdana'>
                            <div>&nbsp;<span
                                    class='celltext'>异常情况</span>
                            </div>
                        </font>
                    </td>
                </tr>
                {}
            </tbody>
        </table>
    """

    rows = []
    loopindex = 1
    for meeting in meetings:
        #
        # 序号
        #  项目名称
        #  所属指南
        #  答辩日期
        #  答辩时间
        #  负责人
        #  联系电话
        #  异常情况

        table_content = """
                    <tr>
                        <td width='12%' nowrap=''>{}</td>
                        <td width='12%' nowrap=''>{}</td>
                        <td width='12%' nowrap=''>{}</td>
                        <td width='12%' nowrap=''>{}</td>
                        <td width='12%' nowrap=''>{}</td>
                        <td width='12%' nowrap=''>{}</td>
                        <td width='12%' nowrap=''>{}</td>
                        <td width='12%' nowrap=''>{}</td>
                    </tr>
                    """.format(
            loopindex, meeting.m_name, meeting.m_guide, meeting.m_date,
            (meeting.m_stime.strftime("%H:%M") + " - " +
             meeting.m_etime.strftime("%H:%M")) + meeting.m_mp +
            meeting.m_mobile + meeting.m_symbol)
        rows.append(table_content)
        loopindex = loopindex + 1
    mail_content.format(getweekdayinfo(), ('').join(rows))

    msg = MIMEText(mail_content, "html", 'utf-8')
    msg["Subject"] = Header('weekplan', 'utf-8')
    msg["From"] = sender_mail
    msg["To"] = 'weekplan'
    try:
        #ssl登录
        smtp = SMTP_SSL(host_server)
        #set_debuglevel()
        smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender, pwd)
        smtp.sendmail(sender_mail, receivers, msg.as_string())
        smtp.quit()
        return True
    except smtplib.SMTPException:
        traceback.print_exc()
        return False
