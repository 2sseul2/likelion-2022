# 메일 보내기

import smtplib
from email.message import EmailMessage
#이미지 확장자 판단
import imghdr 
#정규표현식; regurlar expression
import re

#서버주소, 포트번호
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def sendEmail(addr):
    #유효성 검사
    reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"
    if bool(re.match(reg, addr)):
        # 메일 보내기
        smtp.send_message(message)
        print("정상적으로 메일이 발송되었습니다.")
    else:
        print("유효한 이메일 주소가 아닙니다.")


# 이메일을 만든다
message = EmailMessage()

# 이메일에 내용을 담는다
#MIME - Content
message.set_content("""
코드라이언 수업 중입니다. 
ㅎㅎ
""")

#MIME - Header
message["Subject"]="제목"
message["From"]="###@gmail.com"
message["To"]="###@gmail.com"


# close() 없이도 닫아준다.
with open("codelion.png", "rb") as image:
    image_file = image.read()

# 확장자 판단
image_type = imghdr.what("codelion", image_file)

#첨부파일 
message.add_attachment(image_file,  maintype="image", subtype=image_type)
    
#원하는 서버에 연결한다
smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

#로그인하기
smtp.login("###@gmail.com", "###")

sendEmail("###@gmail.com")
smtp.quit()
