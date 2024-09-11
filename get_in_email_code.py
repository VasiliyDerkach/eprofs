import imaplib
import email
import re
import deltatime_in_email
def get_in_email_code(imap_server,username,in_mail_name,password,priod_sec,now_timezone):
    # Создание подключения и авторизация
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    # Выбор почтового ящика
    mail.select("inbox")
    # Поиск непрочитанных сообщений
    status, response = mail.search(None, "UNSEEN")
    # Обработка найденных сообщений
    unread_msg_nums = response[0].split()
    for msg_num in unread_msg_nums:
        _, msg_data = mail.fetch(msg_num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        emaildate = email.header.decode_header(msg["Date"])[0][0]#.decode('utf-8')
        if deltatime_in_email(emaildate,now_timezone)>priod_sec:
            continue
        subject = email.header.decode_header(msg["Subject"])[0][0].decode('utf-8')
        emailfrom = email.header.decode_header(msg["From"])[1][0].decode('utf-8')
        # print(f"Непрочитанное сообщение с темой: {subject}")
        # print(f"от: {emailfrom} {emaildate}")
        if msg.is_multipart():
            #print("Multipart: Yes")
            for part in msg.walk():
                payload = part.get_payload(decode=True)#.decode()

        else:
            #print("Multipart: No")
            payload = msg.get_payload(None)

        txt = payload.split()
        #print('txt=\n',txt.decode('utf-8'))
        content_type = msg.get_content_type()
        #print('content_type ',content_type)
        po = None
        pk1 = None
        pk = None
        for t in txt:

            pk = t.decode('utf-8').find(', '+in_mail_name + '!')
            if pk>0:
                pk1 = pk
            po = re.search('(?<=' + 'авторизуетесь.<br><br><b><b>' + ').*?(?=</b></b><br><br><b>Если)', t.decode('utf-8'))
            if po and pk1:
                return emailfrom,subject,emaildate,po.group(0)
        if not po:
            return None

    mail.logout()
if __name__=='__main__':
    a,b,c,d = get_in_email_code(imap_server = "imap.mail.ru",username = "profsadokate@mail.ru",password = "BpKrex5kd9pv82aai5FW",
                                priod_sec=600, now_timezone=5)
    print(a,b,c,d)
