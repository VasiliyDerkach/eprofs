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
        deltatm = deltatime_in_email.deltatime_in_email(emaildate,now_timezone)
        if deltatm>priod_sec:
            continue
        subject = email.header.decode_header(msg["Subject"])[0][0].decode('utf-8')
        fr = email.header.decode_header(msg["From"])
        if fr:
            print(fr)
            try:
                emailfrom = fr[1][0].decode('utf-8') #периодическая ошибка поиска
            except:
                print('В письме с кодом не найден From [1][0]')
                print('fr[0]=',fr[0])
                emailfrom = fr[0][0]#.decode('utf-8')
                print('emailfrom=',emailfrom)

        else:
            print(msg)
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
        for i,t in enumerate(txt):
            tx = t.decode('utf-8')
            pk = tx.find(in_mail_name + '&#33;<br><br>')

            # pk = tx.find(in_mail_name )
            # print(i,tx)
            # if i==71:
            #     print(pk)
            if pk==0:
                pk1 = pk
                print(f'Найден {in_mail_name}')
            else:
                print(f'Не найден {in_mail_name}')
            po = re.search('(?<=' + 'авторизуетесь.<br><br><b><b>' + ').*?(?=</b></b><br><br><b>Если)', t.decode('utf-8'))
            # брать строки из настройки
            if po:
                print(f'найден код {po.group(0)}')
            if po and pk1==0:
                return emailfrom,subject,emaildate,po.group(0)
        if not po:
            return None

    mail.logout()
if __name__=='__main__':
    a= get_in_email_code(imap_server = "imap.mail.ru",username = "profsadokate@mail.ru",
                                in_mail_name='Tradeunion', password = "BpKrex5kd9pv82aai5FW",
                                priod_sec=6000, now_timezone=5)
    print(a)
# [('VK <admin@notify.vk.com>', None)] при ошибке from
# [(b'\xd0\x92\xd0\x9a\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb0\xd0\xba\xd1\x82\xd0\xb5', 'utf-8'), (b' <admin@notify.vk.com>', None)]