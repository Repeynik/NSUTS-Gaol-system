import bogdan
import input as myinput
import output

import psycopg2

try:
    conn = psycopg2.connect(dbname='NSUTS', user='postgres', password='123', host='127.0.0.1')

except:
    print("CHIENNE NE RABOTAET CONNECTION. YOUR SERVER IS EVEN ALIVE??")

cursor = conn.cursor()

# cursor.execute('SELECT * FROM SOLUTIONS')
# records = cursor.fetchall()


# for r in records:
#     print(r)
    #(f"{r.Sol_ID}\t {r.User_ID}\t {r.Task_ID}\t {r.Sol_Path}\t {r.Verdict_Final}")
sol_id = 0
while True:
    
    last = bogdan.spam(sol_id, 10)

    myinput.throw(cursor, sol_id, last)

    ls = output.sendtest(sol_id, last)

    input.update(cursor, ls)

    

    print("write 1 to stop")
    isStop = input()
    if isStop:
        break
    
    


cursor.close()
conn.close()