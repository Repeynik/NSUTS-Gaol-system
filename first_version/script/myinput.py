def throw(cursor, sol_id):
    QUERY = f"""
    INSERT INTO QUEUE (sol_id, user_id, competition_id, task_id, verdict_first, verdict_second)
    VALUES ({sol_id}, 12, 1, 1, NULL, NULL); 
    """
    cursor.execute(QUERY)

# def update(cursor, sol_id, verd):
#     QUERY = f"""
#     UPDATE QUEUE
#     SET verdict = "{verd}"
#     WHERE sol_id = {sol_id};
#     """
#     cursor.execute(QUERY)

def print_all(cursor):
    QUERY = f"""
    SELECT * FROM QUEUE;
    """
    cursor.execute(QUERY)
    records = cursor.fetchall()

    for r in records:
        print(r)

def take_verdict_first(cursor, sol_id):
    QUERY = f"""
    SELECT verdict_first
    FROM QUEUE
    WHERE sol_id = {sol_id};
    """
    cursor.execute(QUERY)
    record = cursor.fetchone()

    return record[0]
