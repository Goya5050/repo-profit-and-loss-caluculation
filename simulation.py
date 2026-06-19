from dataclasses import dataclass
import random
import csv
import pulp
import copy
import math

fm1 = "MonsterList_tire1.csv"
fm2 = "MonsterList_tire2.csv"
fm3 = "MonsterList_tire3.csv"
fw = "WeaponList.csv"
fc = "CrystalCostList.csv"

weapon_1 = "prodzap"
weapon_2 = "boltzap"
weapon_3 = "fryingpan"

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

def search_weapon(fname,w1,w2,w3):

    with open(fname,newline="",encoding="utf-8")as f:

        selected_weapon_list = []
        reader = csv.DictReader(f)
        for row in reader :
            if row["name"].lower() == w1.lower() or row["name"].lower() == w2.lower() or row["name"].lower() == w3.lower():
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

def orb_generation(cost,name,orb,count):
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
        print(f"{name}の${profit}Kのオーブが壊れました")
        profit = 0
    elif(luck == 2)or(luck == 3):
        print(f"{name}の${profit}Kのオーブが傷つきました")
        profit = profit/2
    else:
        print(f"{name}の${profit}Kのオーブが無事でした")
        
    return profit

def profit_calculation(monster_list):
    phase_profits = 0
    profits_list = [0,0,0]
    
    for i in range(3):
        print("=========================================")
        print(f"{i+1}フェーズの戦滅報酬")
        for monster in monster_list:
            phase_profits += orb_generation(monster.cost,monster.name,monster.orb,i+1)
        
        profits_list[i] = phase_profits
        print("-----------------------------------------")
        print(f"{i+1}フェーズ目までの収益${profits_list[i]}")
    
    print("==========================================")

    return profits_list

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
    print(f"フェーズ1ごと消費エネルギーは{energy_loss}です。")

    return energy_loss

def loss_calc(fname,level,energyloss):
    
    if(level>=20):
        level = 19
        
    with open(fname,encoding="utf-8")as f:
        crylst = list(csv.reader(f))
        crysct = crylst[level]
        cost_list = [0,0,0]
        shop_list = [0,0,0,0,0]
        
        for i in range(5):
            if random.randint(1,10) <= 5:
                shop_list[i] = int(crysct[1])
            else:
                shop_list[i] = int(crysct[2])
        shop_list = sorted(shop_list, reverse=True)
        print(shop_list)
        
    for i in range(3):
        print(f"フェーズ{i+1}のクリスタル損失を計算しています…")
        copy_list = copy.copy(shop_list)
        for j in range((round(energyloss * (i+1)))):
            cost_list[i] += 1000*int(copy_list.pop())
            
            if not copy_list:
                for j in range(round(energyloss * (i+1))-j):
                    print("品切れしたため、追加購入しました")
                    cost_list[i] += int(crysct[2])
                break
    
    return cost_list



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

"""main"""

print("どのレベルをプレイしたいですか？\n")

simulation_level = int(input())

if simulation_level >= 20:
    simulation_level=20
    print("最高難易度にセットされました\n")
if simulation_level < 0:
    simulation_level=0
    print("0にセットされました\n")

currentlv = spawning_rule("LevelList.csv")

monster_ls = spawn(currentlv.cost1,currentlv.cost2,currentlv.cost3)
weapon_ls = search_weapon(fw,weapon_1,weapon_2,weapon_3)
profit_list = profit_calculation(copy.copy(monster_ls))
loss_list = loss_calc(fc,currentlv.level,energy_calc(monster_ls,weapon_ls))

print(f"1フェーズ目の収益:${profit_list[0]}\n2フェーズ目の収益:${profit_list[1]}\n3フェーズ目の収益:${profit_list[2]}")
print(f"1フェーズの損失:${loss_list[0]}\n2フェーズの損失:${loss_list[1]}\n3フェーズの損失:${loss_list[2]}\n")
print(f"-------------------------------------------")
print("損益結果")
for i in range(3):
    print(f"フェーズ{i+1}回目までの損益(profit/loss):{profit_list[i]/loss_list[i]}")
