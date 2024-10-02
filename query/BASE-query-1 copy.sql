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
verdict_first varchar (255),
verdict_second varchar (255) -- not NULL only if verdict_first is TimeLimit
);
--GO
CREATE TABLE SOLUTIONS
(
sol_id int PRIMARY KEY,
user_id int,
competition_id int,
task_id int,
verdict varchar (255)
);
--GO
CREATE TABLE USERS
(
User_ID int PRIMARY KEY,
User_Name varchar (255) NOT NULL
);
--GO
CREATE TABLE TASKS
(
    Task_ID int PRIMARY KEY,
    Competition_Name varchar(255),
    Task_Name varchar(255),
    Tests_Path varchar(255) -- its will be path to some dirrectory with tests (and maybe limits for tests or limits will be in tests included)
);
--GO
CREATE TABLE MACHINES --?? this can be fully implemented on taker 'script' logic (so mostly useless and time consuming table (only on prototype phase have some benefits))
(
Machine_ID int PRIMARY KEY, 
Sol_ID int, -- some int if machine have solution else NULL if machine is free
Is_Dedicated BIT -- bit == boolean (1, 0, NULL)
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

-- DELETE FROM SOLUTIONS WHERE Sol_ID = 2;
-- GO


--DROP TABLE SOLUTIONS;
--GO

--DROP DATABASE NSUTS;
--GO