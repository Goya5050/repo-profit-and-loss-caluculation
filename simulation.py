from dataclasses import dataclass
import random
import csv
import linecache

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
    
all_weapons = [
    Weapon("Sledge Hammer",10,150,40),
    Weapon("Frying Pan",15,15,12),
    Weapon("Baseball Bat",20,20,15),
    Weapon("Hand Gun",20,80,20),
    Weapon("Photon Blaster",8,225,40)
]
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

def spawning(fname):
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
for i in range(current.cost1):
    enemy=spawning(fm1)
    print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
    if enemy.orb == 1:
        print("出現する")
    else:
        print("出現しない")
for i in range(current.cost2):
    enemy=spawning(fm2)
    print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
    if enemy.orb == 1:
        print("出現する")
    else:
        print("出現しない")
for i in range(current.cost3):
    enemy=spawning(fm3)
    print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
    if enemy.orb == 1:
        print("出現する")
    else:
        print("出現しない")

    


        




