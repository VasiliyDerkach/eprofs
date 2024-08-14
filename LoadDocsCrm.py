import re

result = re.search('(?<=Path=).*?(?=\n)', 'Path=D:/yand/\n')
print(result.group(0) if result else "Текст между маркерами не найден.")