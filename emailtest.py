import imaplib
import email
import re

# Параметры для подключения к IMAP-серверу
imap_server = "imap.mail.ru"
username = "profsadokate@mail.ru"
password = "BpKrex5kd9pv82aai5FW"

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
    subject = email.header.decode_header(msg["Subject"])[0][0].decode('utf-8')
    emailfrom = email.header.decode_header(msg["From"])[1][0].decode('utf-8')
    emaildate = email.header.decode_header(msg["Date"])[0][0]#.decode('utf-8')

    print(f"Непрочитанное сообщение с темой: {subject}")
    print(f"от: {emailfrom} {emaildate}")
    if msg.is_multipart():
        print("Multipart: Yes")
        for part in msg.walk():
            payload = part.get_payload(decode=True)#.decode()

    else:
        print("Multipart: No")
        payload = msg.get_payload(None)

    txt = payload.split()
    #print('txt=\n',txt.decode('utf-8'))
    content_type = msg.get_content_type()
    print('content_type ',content_type)
    for t in txt:
        po = re.search('(?<=' + 'авторизуетесь.<br><br><b><b>' + ').*?(?=</b></b><br><br><b>Если)', t.decode('utf-8'))
        if po:
            print(po.group(0))
    # for msg in pop3.list()[1]:
    #     for line in pop3.retr(msg.split()[0])[1]:
    #         print
    #         unicode(line, 'koi8-r').encode('cp1251')
    # print('text-\n',payload)
    #print(msg)

mail.logout()