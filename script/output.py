import tester

def sendtest(sol_id, last):
    ls = list
    for i in range(sol_id, last):
        str = tester.test(i)
        ls.append(str)
    return ls


def sendretest(sol_id, last):
    ls = list
    for i in range(sol_id, last):
        str = tester.test(i)
        ls.append(str)
    return ls