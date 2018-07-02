#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-4-06


@module: MyMAIL
@used: send mail
"""

import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


from MyLOG import MyLog
from botasky.utils.MyFILE import project_abdir, recursiveSearchFile
logConfig = recursiveSearchFile(project_abdir, '*logConfig.ini')[0]
mylog = MyLog(logConfig, 'MyMAIL.py')
logger = mylog.outputLog()


__all__ = ['MyMail']
__author__ = 'zhihao'

mail_info = {'mail_host': 'smtp.163.com',
             'mail_user': '15895890858',
             'mail_pass': 'zhi@hao@111',
             'mail_postfix': '163.com'}


class MyMail():
    '''
    used : send mail
    '''
    def __init__(self, mail_info):
        '''
        used : init mail
        :param mail_info: smtp server config
        '''
        self.mail_info = mail_info

    def send_mail(self, to_list, mail_type, subject, content, attachment_list, img_list):
        '''
        used : send mail
        :param to_list: target mail adresses
        :param mail_type: plain or html
        :param subject: title
        :param content: main body
        :param attachment_list: attachment
        :param img_list: picture
        :return:
        '''
        my_adress = "0905zhihao" + "<" + self.mail_info['mail_user'] + "@" + self.mail_info['mail_postfix'] + ">"

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = my_adress
        msg['To'] = ";".join(to_list)

        #main text
        if mail_type == 'plain' or mail_type == 'html':
            try:

                body_msg = MIMEText(content, _subtype=mail_type, _charset='gb2312')
                msg.attach(body_msg)

                exec_info = "[action]:init msg" \
                            "[status]:OK" \
                            "[Subject]:{Subject}" \
                            "[From]:{From}" \
                            "[To]:{To}".format(Subject=msg['Subject'], From=msg['From'], To=msg['To'])
                logger.info(exec_info)

            except Exception, e:
                print Exception, ":", e
                error_msg = "[action]:init msg" \
                            "[status]:FAIL" \
                            "[Errorcode]:{e}" \
                            "[Subject]:{Subject}" \
                            "[From]:{From}" \
                            "[To]:{To}".format(Subject=msg['Subject'], From=msg['From'], To=msg['To'], e=e)
                logger.error(error_msg)

        else:

            error_msg = "[action]:send mail_type" \
                        "[status]:FAIL" \
                        "[Errorcode]mail_type is not format" \
                        "[Subject]:{Subject}" \
                        "[From]:{From}" \
                        "[To]:{To}".format(Subject=msg['Subject'], From=msg['From'], To=msg['To'])

            print error_msg
            logger.info(error_msg)

        #attachment
        if attachment_list == '' or len(attachment_list) == 0:
            pass
        else:
            for attachment in attachment_list:
                try:
                    att = MIMEText(open(attachment, 'rb').read(), 'base64', 'gb2312')
                    att["Content-Type"] = 'application/octet-stream'
                    #display name
                    att["Content-Disposition"] = 'attachment; filename="'+attachment+'\"\''
                    msg.attach(att)

                    exec_info = "[action]:add attachment" \
                                "[status]:OK" \
                                "[attachment]:{attachment}" \
                                "[Subject]:{Subject}" \
                                "[From]:{From}" \
                                "[To]:{To}".format(attachment=attachment, Subject=msg['Subject'],
                                                   From=msg['From'], To=msg['To'])
                    logger.info(exec_info)

                except Exception, e:
                    print Exception, ":", e
                    error_msg = "[action]:add attachment" \
                                "[status]:FAIL" \
                                "[Errorcode]:{e}" \
                                "[attachment]={attachment}" \
                                "[Subject]:{Subject}" \
                                "[From]:{From}" \
                                "[To]:{To}".format(Subject=msg['Subject'], From=msg['From'],
                                                   attachment=attachment, To=msg['To'], e=e)
                    logger.error(error_msg)

        #img
        if img_list == '' or len(img_list) == 0:
            pass
        else:
            for image_adress in img_list:
                try:
                    image = MIMEImage(open(image_adress, 'rb').read())
                    image.add_header('Content-ID', '<image1>')
                    msg.attach(image)

                    exec_info = "[action]:add image" \
                                "[status]:OK" \
                                "[image]:{image}" \
                                "[Subject]:{Subject}" \
                                "[From]:{From}" \
                                "[To]:{To}".format(image=image_adress, Subject=msg['Subject'],
                                                   From=msg['From'], To=msg['To'])
                    logger.info(exec_info)

                except Exception, e:

                    print Exception, ":", e
                    error_msg = "[action]:add image" \
                                "[status]:FAIL" \
                                "[Errorcode]:{e}" \
                                "[image]:{image}" \
                                "[Subject]:{Subject}" \
                                "[From]:{From}" \
                                "[To]:{To}".format(Subject=msg['Subject'], From=msg['From'],
                                                   image=image_adress, To=msg['To'], e=e)
                    logger.error(error_msg)


        #send mail
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_info['mail_host'])
            server.login(self.mail_info['mail_user'], self.mail_info['mail_pass'])
            server.sendmail(msg['from'], msg['to'], msg.as_string())
            server.quit()

            exec_info = "[action]:send mail" \
                        "[status]:OK" \
                        "[Subject]:{Subject}" \
                        "[From]:{From}" \
                        "[To]:{To}".format(Subject=msg['Subject'], From=msg['From'],To=msg['To'])
            logger.info(exec_info)
        except Exception, e:
            print Exception, ":", e
            error_msg = "[action]:send mail" \
                        "[status]:FAIL" \
                        "[Errorcode]:{e}" \
                        "[Subject]:{Subject}" \
                        "[From]:{From}" \
                        "[To]:{To}".format(Subject=msg['Subject'], From=msg['From'], To=msg['To'], e=e)
            logger.error(error_msg)


if __name__ == '__main__':
    '''
    mail_info = {'mail_host': 'smtp.163.com',
                 'mail_user': '15002283621',
                 'mail_pass': 'zhihao1206',
                 'mail_postfix': '163.com'}


    #to_list = ['15002283621@163.com']
    to_list = ['1204207658@qq.com']
    subject = 'xxxxxxxxxxxxx'
    content = 'xxxxxxxxxxxxx'
    #attachment_list = ['F:\img\img.rar', 'F:\img\img2.rar']
    attachment_list = []
    #img_list = ['F:\img\\1025.jpg', 'F:\img\\1041.jpg']
    img_list = []
    mail = MyMail(mail_info)
    mail.send_mail(to_list, 'plain', subject, content, attachment_list, img_list)
    '''
    import MyMAIL
    help(MyMAIL)






