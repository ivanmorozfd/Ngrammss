import psycopg2
import re
from psycopg2 import sql
#-----------------------------------------------------------------------
#функция , возвращающая список N-грамм
#input_list - строка
#n - размерность
def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])
#-----------------------------------------------------------------------
#конверт кортежа в строку
def convertTuple(tup):
    str =  ''.join(tup)
    return str
#-----------------------------------------------------------------------
#Обрабатываем текст из файла, переводим в апперкейс и прогоняем регуляркой
pattern = "[^А-Я0-9.,!?:\"%-+=/]"
f = open('text.TXT', 'r+',encoding='utf-8')
text = f.read()
text = text.upper()
result = re.sub(pattern,'',text)
f.close();
#-----------------------------------------------------------------------
#Пишем результат в файл
f = open('resultText.txt','w',encoding='utf-8');
f.write(result);
f.close()
#-----------------------------------------------------------------------
#Работаем с бд: открываем коннект, объявляем курсор
print("\n Введите пароль к базе")
password = input()

conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password=password, host='localhost')

cursor = conn.cursor()
#-----------------------------------------------------------------------
#чистим базу перед использованием
cursor.execute("truncate table letters restart identity")
cursor.execute("truncate table  bigrams restart identity")
cursor.execute("truncate table  trigrams restart identity")
cursor.execute("truncate table  quadgrams restart identity")
#-----------------------------------------------------------------------
# пишем в базу посимвольно
for i in result:
    cursor.execute("INSERT INTO letters(value) VALUES('{}')".format(i))
# 2 - граммы
query  = "INSERT INTO"
bigramms = find_ngrams(result,2)
for i in bigramms:
    cursor.execute("INSERT INTO bigrams(value) VALUES('{}')".format(convertTuple(i)))
# 3 - граммы
trigramms = find_ngrams(result,3)
for i in trigramms:
    cursor.execute("INSERT INTO trigrams(value) VALUES('{}')".format(convertTuple(i)))
#4 - граммы
quadgramms = find_ngrams(result,4)
for i in quadgramms:
    cursor.execute("INSERT INTO quadgrams(value) VALUES('{}')".format(convertTuple(i)))

conn.commit()
count = 0
#-----------------------------------------------------------------------
#открываем файл для записи статистики
f = open("ngramms.txt","w+",encoding="utf-8")
#-----------------------------------------------------------------------
# Извлекаем статистику и пишем ее в файл
# Символы
cursor.execute("SELECT COUNT(*) FROM letters")
count = cursor.fetchone()
cursor.execute("SELECT COUNT (value) AS Count, value AS Value FROM letters GROUP BY value ORDER BY Count DESC ")
rows = cursor.fetchall()
for row in rows:
    f.write("{};{};{}\n".format(row[1],row[0],count[0]))
# 2 - граммы
cursor.execute("SELECT COUNT(*) FROM bigrams")
count = cursor.fetchone()
cursor.execute("SELECT COUNT (value) AS Count, value AS Value FROM bigrams GROUP BY value ORDER BY Count DESC ")
rows = cursor.fetchall()
for row in rows:
    f.write("{};{};{}\n".format(row[1],row[0],count[0]))
# 3 - граммы
cursor.execute("SELECT COUNT(*) FROM trigrams")
count = cursor.fetchone()
cursor.execute("SELECT COUNT (value) AS Count, value AS Value FROM trigrams GROUP BY value ORDER BY Count DESC")
rows = cursor.fetchall()
for row in rows:
    f.write("{};{};{}\n".format(row[1],row[0],count[0]))
# 4 - граммы
cursor.execute("SELECT COUNT(*) FROM quadgrams")
count = cursor.fetchone()
cursor.execute("SELECT COUNT (value) AS Count, value AS Value FROM quadgrams GROUP BY value ORDER BY Count DESC")
rows = cursor.fetchall()
for row in rows:
    f.write("{};{};{}\n".format(row[1],row[0],count[0]))

