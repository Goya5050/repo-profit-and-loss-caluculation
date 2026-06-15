from dataclasses import dataclass

@dataclass
class Weapon:
    name: str
    energy: int
    damage: int
    cost: int

@dataclass
class Monster:
    name : str
    health : int
    cost : int
    Orb : int

@dataclass
class Levelset:
    level : int
    cost3 : int
    cost2 : int
    cost1 : int



all_weapons = [
    Weapon("Sledge Hammer",10,150,40),
    Weapon("Frying Pan",15,15,12),
    Weapon("Baseball Bat",20,20,15),
    Weapon("Hand Gun",20,80,20),
    Weapon("Photon Blaster",8,225,40)
]

all_enemies = [
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
]

tier1_enemies = [enemy for enemy in all_enemies if enemy.cost == 1]

tier2_enemies = [enemy for enemy in all_enemies if enemy.cost == 2]

tier3_enemies = [enemy for enemy in all_enemies if enemy.cost == 3]



