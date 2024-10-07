--CREATE DATABASE NSUTS;
--GO
--USE NSUTS
--GO
CREATE TABLE QUEUE
(
sol_id int PRIMARY KEY,
user_id int,
competition_id int,
task_id int,
sol_blob bytea,
is_testing BOOLEAN,
is_timeout BOOLEAN
);
--GO			
CREATE TABLE SOLUTIONS
(
sol_id int PRIMARY KEY,
user_id int,
competition_id int,
task_id int,
sol_blob bytea,
verdict varchar (255)
);
--GO
CREATE TABLE USERS
(
user_id int PRIMARY KEY,
user_name varchar (255) NOT NULL
);
--GO
CREATE TABLE TASKS
(
competition_id int PRIMARY KEY,
competition_name varchar(255),
task_id int,
task_name varchar(255),
tests_blob bytea
);
--GO
CREATE TABLE MACHINES --?? this can be fully implemented on taker 'script' logic (so mostly useless and time consuming table (only on prototype phase have some benefits))
(
machine_id int PRIMARY KEY, 
sol_id int, -- some int if machine have solution else NULL if machine is free
is_dedicated BOOLEAN -- boolean (TRUE, FALSE, NULL)
);
--GO
INSERT INTO SOLUTIONS (Sol_ID, User_ID, Task_ID, Sol_Path, Verdict_Final)
VALUES
    (1, 0, 1, '/sol/1', NULL),
    (2, 0, 1, '/sol/2', NULL),
    (3, 0, 2, '/sol/3', NULL)
;
--GO
UPDATE SOLUTIONS
SET Verdict_Final = 'Accepted'
WHERE Sol_ID = 1;
--GO
UPDATE SOLUTIONS
SET Verdict_Final = 'Wrong answear'
WHERE Sol_ID = 1;
--GO
SELECT * FROM SOLUTIONS;
--GO
SELECT * FROM QUEUE;

INSERT INTO QUEUE (sol_ID, User_ID, competition_id, Task_ID, sol_blob, Verdict_first, verdict_second)
VALUES
    (2, 0, 1, 1, '\x01', NULL, NULL)
;

-- 	SELECT * FROM QUEUE WHERE verdict_first IS NULL LIMIT 1;

-- -- DELETE FROM SOLUTIONS WHERE Sol_ID = 2;
-- -- GO

-- SELECT * FROM QUEUE WHERE is_timeout IS NULL LIMIT 1;

-- SELECT * FROM QUEUE WHERE is_timeout IS NULL AND is_testing IS False LIMIT 1;


-- DROP TABLE QUEUE;
--GO

--DROP DATABASE NSUTS;
--GO