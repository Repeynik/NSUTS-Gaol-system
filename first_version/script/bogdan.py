import random

import os, glob
import errno

def clear():
    for file in glob.glob("script/solutions/*"):
        os.remove(file)

def spam(sol_id, len):

    # create dir solutions
    path = "script/solutions/"
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    # make random .txt files as solutions
    for i in range(sol_id, len):
        #print(i)
        try:
            with open(f'{path}/sol{i}.txt', 'x') as f:
                num = random.randint(0,10000)
                f.write(str(num))
        except FileExistsError:
            print("WHY FILE ALREADY EXIST??? DELETE IT")
    return sol_id + len