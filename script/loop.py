import bogdan
import myinput
import output

import psycopg2

try:
    conn = psycopg2.connect(dbname='NSUTS', user='postgres', password='123', host='127.0.0.1')

except:
    print("CHIENNE NE RABOTAET CONNECTION. YOUR SERVER IS EVEN ALIVE??")

cursor = conn.cursor()

#delete past
cursor.execute("DELETE FROM QUEUE;")

# cursor.execute('SELECT * FROM SOLUTIONS')
# records = cursor.fetchall()


# for r in records:
#     print(r)
    #(f"{r.Sol_ID}\t {r.User_ID}\t {r.Task_ID}\t {r.Sol_Path}\t {r.Verdict_Final}")
sol_id = 0
step = 10
# delete past solutions
bogdan.clear()
while True:
    #print(sol_id, sol_id+step)
    bogdan.spam(sol_id, sol_id+step)

    for i in range (sol_id, sol_id + step):
        #print(i)
        myinput.throw(cursor, i)
    
    # debug
    #myinput.print_all(cursor)
    output.send_test(cursor, sol_id, sol_id + step)

    for i in range(sol_id, sol_id + step):
        ss = myinput.take_verdict_first(cursor, i)
        #print(ss, ss == 'time limit', i)
        if ss == 'time limit':
            output.send_retest(cursor, i)

    

    # myinput.update(cursor, ls)

    
    sol_id += step
    print("write 1 to stop")
    isStop = input()
    if isStop == '1':
        break
    
    

conn.commit()
cursor.close()
conn.close()