from dataclasses import dataclass
import random
import csv
import pulp
import copy
import math

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

@dataclass
class Weapon_info:
    name: str
    damage: int
    mincost: int
    maxcost: int
    energy: int
    
@dataclass
class Weapons:
    w1 : Weapon_info
    w2 : Weapon_info
    w3 : Weapon_info

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
    with open(fname, encoding="utf-8") as f:
        levelsets = list(csv.reader(f))

        levelset = levelsets[simulation_level-1]

        current_rule = Levelset(
            level=simulation_level,
            cost1=int(levelset[0]),
            cost2=int(levelset[1]),
            cost3=int(levelset[2])
        )

    return current_rule

def search_weapon(fname,w1,w2,w3):

    with open(fname,newline="",encoding="utf-8")as f:

        selected_weapon_list = []
        reader = csv.DictReader(f)
        for row in reader :
            if row["name"] == w1 or row["name"] == w2 or row["name"] == w3:
                ##js側で被らないように設定しておく
                weapon = Weapon_info(
                    name = row["name"],
                    damage=int(row["damage"]),
                    mincost=int(row["mincost"]),
                    maxcost=int(row["maxcost"]),
                    energy=int(row["energy"])
                )

                selected_weapon_list.append(weapon)

    
    return selected_weapon_list


def spawning_monster(fname):
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

def orb_generation(cost,orb):
    if orb == 0:
        return 0
    match cost:
        case 1: 
            profit = random.randrange(2000,3001,100)
        case 2:
            profit = random.randrange(3500,4501,100)
        case 3:
            profit = random.randrange(5500,7501,100)
    luck = random.randint(1,10)
    if(luck == 1):
        print(f"${profit}Kのオーブが壊れました")
        profit = 0
    elif(luck == 2)or(luck == 3):
        print(f"${profit}Kのオーブが傷つきました")
        profit = profit/2
        

    return profit

def profit_calculation(monster_list):
    all_profits = 0
    phase_profit = [0,0,0]
    while monster_list:
        monster = monster_list.pop()
        for i in range(3):
            phase_profit[i]+=orb_generation(monster.cost,monster.orb)

    all_profits = phase_profit[0]+phase_profit[1]+phase_profit[2]
    phase2_profits = phase_profit[0]+phase_profit[1]

    print(f"1フェーズ目の収益は${phase_profit[0]}")
    print(f"2フェーズ目の収益は${phase_profit[1]}")
    print(f"3フェーズ目の収益は${phase_profit[2]}")
    print("----------------------------------------")
    print(f"全収益は${all_profits} 2フェーズまでの収益は${phase2_profits} ")


def energy_calc(monster_list,weapon_list):
    weapon_1 = weapon_list.pop()
    weapon_2 = weapon_list.pop()
    weapon_3 = weapon_list.pop()
    energy_loss = 0.0

    while monster_list:
        usage = 0.0
        monster = monster_list.pop()
        usage = math.ceil(optimizing(weapon_1.damage,weapon_2.damage,weapon_3.damage,monster.health,1/weapon_1.energy,1/weapon_2.energy,1/weapon_3.energy)*100)/100
        energy_loss += usage
        print(f"{monster.name}を倒すのに{usage}エネルギーを使いました")
    print(f"消費したエネルギーは{energy_loss}です。")


def spawn(cost1,cost2,cost3):

    floor_monsters: list[Monster] = []
    for _ in range(cost1):
        enemy=spawning_monster(fm1)
        floor_monsters.append(enemy)
        print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
        if enemy.orb == 1:
            print("出現する")
            ##Phase_profits,all_profits+=profit_cal(enemy.cost)
        else:
            print("出現しない")

    for _ in range(cost2):
        enemy=spawning_monster(fm2)
        floor_monsters.append(enemy)
        print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
        if enemy.orb == 1:
            print("出現する")
            ##Phase_profits,all_profits+=profit_cal(enemy.cost)
        else:
            print("出現しない")

    for _ in range(cost3):
        enemy=spawning_monster(fm3)
        floor_monsters.append(enemy)
        print(f"{enemy.name}の体力は{enemy.health}であり、ティアは{enemy.cost}、オーブは",end="")
        if enemy.orb == 1:
            print("出現する")
            ##Phase_profits,all_profits+=profit_cal(enemy.cost)
        else:
            print("出現しない")
    
    return floor_monsters
    

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
        energy_loss = float(prob.objective.value())
        print(f"  目的関数値 (ax+by+cz) = {energy_loss}")
        print(f"  制約確認 (Ax+By+Cz)  = {A*xv + B*yv + C*zv} >= {h}")
        return energy_loss
    else:
        print("最適解が見つかりませんでした。")
        return 0.0

fm1 = "MonsterList_tire1.csv"
fm2 = "MonsterList_tire2.csv"
fm3 = "MonsterList_tire3.csv"
fw = "WeaponList.csv"

print("どのレベルをプレイしたいですか？\n")

simulation_level = int(input())

if simulation_level >= 20:
    print("最高難易度にセットされました\n")
if simulation_level < 0:
    print("0にセットされました\n")

currentlv = spawning_rule("LevelList.csv")

print(f"レベルは{currentlv.level}です")

monster_ls = spawn(currentlv.cost1,currentlv.cost2,currentlv.cost3)
weapon_ls = search_weapon(fw,"HandGun","KartCannon","SledgeHammer")
profit_calculation(copy.copy(monster_ls))
energy_calc(monster_ls,weapon_ls)

##optimizing(270,800,0,250,1/5,1/5,1/10)

    


        




