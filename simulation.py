from dataclasses import dataclass
import random
import csv
import pulp

@dataclass
class Weapon:
    name: str
    energy: int
    damage: int
    cost: int

@dataclass
class Levelset:
    level: int
    cost1: int
    cost2: int
    cost3: int

@dataclass
class Monster:
    name : str
    health : int
    cost : int
    orb : int
    
"""all_weapons = [
    Weapon("Sledge Hammer",10,150,40),
    Weapon("Frying Pan",15,15,12),
    Weapon("Baseball Bat",20,20,15),
    Weapon("Hand Gun",20,80,20),
    Weapon("Photon Blaster",8,225,40)
]"""

"""all_enemies = [
    Monster("Robe",250,3,1),
    Monster("Trudge",500,3,1),
    Monster("Clown",250,3,1),
    Monster("Ragrat",150,2,1),
    Monster("Hidden",150,2,1),
    Monster("Cheff",150,2,1),
    Monster("Banger",80,2,0),
    Monster("spewer",65,1,1),
    Monster("Shadow Child",150,1,1),
    Monster("Gnome",65,1,0)
]"""

def spawning_rule(fname):
    with open(fname, encoding="utf-8" ) as f:
        data = None
        for i ,row in enumerate(csv.reader(f),start=1):
            if random.random() < 1 / i:
                data = row

    enemy = Monster(
        name = data[0],
        health = int(data[1]),
        cost = int(data[2]),
        orb = int(data[3])
    )

    return enemy

def spawn(cost1,cost2,cost3):
    for i in range(cost1):
        enemy=spawning_rule(fm1)
        print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
        if enemy.orb == 1:
            print("出現する")
        else:
            print("出現しない")
    for i in range(cost2):
        enemy=spawning_rule(fm2)
        print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
        if enemy.orb == 1:
            print("出現する")
        else:
            print("出現しない")
    for i in range(cost3):
        enemy=spawning_rule(fm3)
        print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
        if enemy.orb == 1:
            print("出現する")
        else:
            print("出現しない")

def optimizing(A,B,C,h,a,b,c):
    
    prob = pulp.LpProblem("efficient_attack_method",pulp.LpMinimize)

    x=pulp.LpVariable("x",lowBound=0,cat="Integer")
    y=pulp.LpVariable("y",lowBound=0,cat="Integer")
    z=pulp.LpVariable("z",lowBound=0,cat="Integer")

    prob += a*x+b*y+c*z , "Objective"

    prob += A*x+B*y+C*z >= h , "Constraint"

    status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
    xv, yv, zv = int(x.value()), int(y.value()), int(z.value())
    

    print("=" * 40)
    print(f"ステータス: {pulp.LpStatus[status]}")
    print("=" * 40)
    
    if pulp.LpStatus[status] == "Optimal":
        xv, yv, zv = int(x.value()), int(y.value()), int(z.value())
        print(f"  x = {xv}")
        print(f"  y = {yv}")
        print(f"  z = {zv}")
        print(f"  目的関数値 (ax+by+cz) = {float(prob.objective.value())}")
        print(f"  制約確認 (Ax+By+Cz)  = {A*xv + B*yv + C*zv} >= {h}")
    else:
        print("最適解が見つかりませんでした。")




print("どのレベルをプレイしたいですか？\n")
simulation_level = int(input())
if simulation_level >= 20:
    print("最高難易度にセットされました\n")
if simulation_level < 0:
    print("0にセットされました\n")


"""print("どのくらいやりますか？")
simulation_time = int(input())"""



with open("levelList.csv", encoding="utf-8") as f:
    levelsets = list(csv.reader(f))

levelset = levelsets[simulation_level-1]

current = Levelset(
    level=simulation_level,
    cost1=int(levelset[0]),
    cost2=int(levelset[1]),
    cost3=int(levelset[2])
)


fm1 = "MonsterList_tire1.csv"
fm2 = "MonsterList_tire2.csv"
fm3 = "MonsterList_tire3.csv"

print(f"レベルは{current.level}です")

##spawn(current.cost1,current.cost2,current.cost3)

optimizing(270,800,0,250,1/5,1/5,1/10)

    


        




