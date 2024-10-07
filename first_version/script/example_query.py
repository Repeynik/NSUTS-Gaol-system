import psycopg2

try:
    conn = psycopg2.connect(dbname='NSUTS', user='postgres', password='123', host='127.0.0.1')

except:
    print("CHIENNE NE RABOTAET CONNECTION. YOUR SERVER IS EVEN ALIVE??")

# try:
#     conn = psycopg2.connect('postgresql://postgres:123@127.0.0.1:5432/NSUTS')
# except:
#     print("CHIENNE NE RABOTAET CONNECTION. YOUR SERVER IS EVEN ALIVE??")

cursor = conn.cursor()

cursor.execute('SELECT * FROM SOLUTIONS')
records = cursor.fetchall()
cursor.close()
conn.close()


for r in records:
    print(r)
    #(f"{r.Sol_ID}\t {r.User_ID}\t {r.Task_ID}\t {r.Sol_Path}\t {r.Verdict_Final}")