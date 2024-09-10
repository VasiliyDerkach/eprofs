import imaplib
import email

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
            payload = part.get_payload(None)

    else:
        print("Multipart: No")
        payload = msg.get_payload(None)
    print('text-\n',payload.encode('utf-8'))
    print(msg)

mail.logout()