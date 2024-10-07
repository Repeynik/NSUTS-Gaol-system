DELETE FROM QUEUE;

DELETE FROM SOLUTIONS;



INSERT INTO QUEUE (sol_id, user_id, competition_id, task_id, sol_blob, is_testing, is_timeout)
VALUES
    (1, 1, 1, 1, 'DEAD' :: bytea, False, NULL),
	(2, 1, 1, 1, 'BEEF' :: bytea, False, NULL),
	(3, 1, 1, 1, 'CEBA' :: bytea, False, NULL),
	(4, 1, 1, 1, 'BACAAAA' :: bytea, False, NULL),
	(5, 1, 1, 1, 'CACADAAA' :: bytea, False, NULL)
;