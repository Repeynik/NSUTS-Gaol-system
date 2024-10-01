import random

def spam(sol_id, len):
    for i in range(sol_id+len):
        try:
            with open(f'script/solutions/sol{i}.txt', 'x') as f:
                num = random.randint(0,10000)
                f.write(str(num))
        except FileExistsError:
            print("WHY FILE ALREADY EXIST??? DELETE IT")
    sol_id += len
    return sol_id