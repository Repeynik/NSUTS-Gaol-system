def test(sol_id):
    with open(f'script/solutions/sol{sol_id}.txt', 'r') as f:
        num = int(f.read()) % 3
        if num == 0:
            return "accepted"
        elif num == 1:
            return "wrong answear"
        elif num == 2:
            return "time limit"
            
        return "undefined behaviour"

def retest(sol_id):
    with open(f'script/solutions/sol{sol_id}.txt', 'r') as f:
        num = int(f.read()) % 3
        if num == 0:
            return "accepted"
        elif num == 1:
            return "wrong answear"
        elif num == 2:
            return "time limit"
            
        return "undefined behaviour"