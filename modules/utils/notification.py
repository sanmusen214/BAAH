from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from modules.configs.MyConfig import config
from modules.utils.data_utils import decrypt_data


class Message_Sender:
    """
    消息发送的基类
    """
    def send(self, message: str):
        pass
    
class Email_Sender(Message_Sender):
    """
    邮件发送类
    
    Parameters
    ==========
    mail_user: str
        发送者的账号
    mail_pass: str
        发送者的token
    sender: str
        发送者的邮箱
    receiver: str
        接收者的邮箱
    mail_host: str
        邮件服务器地址
    debug_int: int
        调试模式
    """
    def __init__(self, mail_user, mail_pass, sender, receiver, mail_host = 'smtp.qq.com', debug_int = 1):
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.receiver = receiver
        self.mail_host = mail_host
        self.debug_int = debug_int
    
    def send(self, message: str, title: str = "BAAH通知") -> str:
        return self.send_mail(message, title)
        
    def send_mail(self, message, title):
        if self.mail_user == '' or self.mail_pass == '' or self.receiver == '' or self.mail_host == '':
            # 如果没有指定发送者的qq号或者授权码，则直接返回
            return '发送信息不全'
        #ssl登录
        smtp = SMTP_SSL(self.mail_host)
        #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(self.debug_int)
        smtp.ehlo(self.mail_host)
        smtp.login(self.mail_user, self.mail_pass)

        msg = MIMEText(message, "plain", 'utf-8')
        msg["Subject"] = Header(title, 'utf-8')
        msg["From"] = self.sender
        msg["To"] = self.receiver
        res=smtp.sendmail(self.sender, self.receiver, msg.as_string())
        smtp.quit()
        return res

class Notificationer:
    """
    通知类，用于发送通知
    """
    def __init__(self, sender: Message_Sender):
        self.sender = sender

    def send(self, message: str) -> str:
        return self.sender.send(message)

# 实例化放在BAAH的生命周期里，每个配置文件邮箱可以不一样
def create_notificationer():
    """
    创建一个通知器
    """
    # 构造通知对象
    if config.userconfigdict['ADVANCED_EMAIL']:
        # 如果开启了高级模式，则用户自己定义所有的邮件发送参数
        email_sender = Email_Sender(
            config.userconfigdict['MAIL_USER'], 
            decrypt_data(config.userconfigdict['MAIL_PASS'], config.softwareconfigdict["ENCRYPT_KEY"]), 
            config.userconfigdict['SENDER_EMAIL'], 
            config.userconfigdict['RECEIVER_EMAIL'], 
            config.userconfigdict['MAIL_HOST'], 
            1
        )
    else:
        email_sender = Email_Sender(
            config.userconfigdict['MAIL_USER'], 
            decrypt_data(config.userconfigdict['MAIL_PASS'], config.softwareconfigdict["ENCRYPT_KEY"]), 
            config.userconfigdict['MAIL_USER']+"@qq.com", 
            config.userconfigdict['MAIL_USER']+"@qq.com", 
            'smtp.qq.com', 
            1)
    notificationer = Notificationer(email_sender)
    return notificationer