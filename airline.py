def valid(f,g,schedule,flights):
    dep = flights[f]["departure_time"]
    gs = flights[f]["gate_start"]
    ge = flights[f]["gate_end"]
    if not (gs<=dep<=ge):
        return False

    for i in schedule:
        gate = schedule[i]
        if gate == g and i != f: 
            g_start = flights[i]["gate_start"]
            g_end = flights[i]["gate_end"]
            if not (ge<= g_start or gs>= g_end):
                return False
    return True

def fcheck(flights,domains,schedule,f,g):
    for i in flights:
        if i not in schedule: 
            valid_gates=[]
            for gate in domains[i]:
                if valid(i,gate,schedule,flights):
                    valid_gates.append(gate)
            if len(valid_gates) == 0:
                return False
            domains[i] =valid_gates
    return True

def backtrack(flights,gates,schedule,variables,domains):
    if len(schedule) == len(flights): 
        return schedule
    f = variables[0]
    for g in domains[f]:
        schedule[f] = g
        copy_d = {flight: list(domains[flight]) for flight in flights}
        copy_d[f] = [g]
        
        if valid(f,g,schedule,flights) and fcheck(flights,copy_d,schedule,f, g):
            result = backtrack(flights,gates,schedule,variables[1:],copy_d)
            if result:
                return result
        
        schedule.pop(f)
    return None



n_gates = int(input("Enter number of gates: "))
gates = [f"G{i+1}" for i in range(n_gates)]
flights = {}
n = int(input("Enter number of flights: "))
for i in range(n):
    print(f"Enter details for Flight F{i+1}:")
    dep = int(input("Departure Time(in hours): "))
    gs = int(input("Gate Start Time(in hours): "))
    ge = int(input("Gate End Time(in hours): "))
    flights[f"F{i+1}"] = {"departure_time": dep,"gate_start": gs,"gate_end": ge}

schedule = {}
variables = [f"F{i+1}" for i in range(n)]  
domains = {flight: gates[:] for flight in flights}  
result = backtrack(flights, gates, schedule, variables, domains)
if result:
    print("Flight Schedule:")
    for flight in result:
        gate = result[flight]
        print(f"{flight} -> {gate}")
else:
    print("No valid schedule.")
