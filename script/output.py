import tester
import myinput

def send_test(cursor, sol_id, last):
    for i in range(sol_id, last):
        verd = tester.test(i)
        #myinput.update(cursor, sol_id, verd)
        QUERY = f"""
        UPDATE QUEUE
        SET verdict_first = '{verd}'
        WHERE sol_id = {i};
        """
        cursor.execute(QUERY)


def send_retest(cursor, sol_id):
    verd = tester.retest(sol_id)
    #myinput.update(cursor, sol_id, verd)
    QUERY = f"""
    UPDATE QUEUE
    SET verdict_second = '{verd}'
    WHERE sol_id = {sol_id};     
    """
    cursor.execute(QUERY)