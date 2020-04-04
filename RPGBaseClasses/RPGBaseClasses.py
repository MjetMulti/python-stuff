from copy import deepcopy
import json

class Spell:
	"base class for spells"
	def __init__(self):
		self.mana_cost = 0
		self.type = "void"
		self.damage = 0

class Item:
	def __init__(self, weight = 0):
		self.weight = weight

class Weapon(Item):
	def __init__(self, weight = 0, attack = 1):
		super().__init__(weight)
		self.attack = attack
		
class Armor(Item):
	def __init__(self, weight = 0, defense = 0, slot = "Body"):
		super().__init__(weight)
		self.defense = defense
		self.slot = slot
		
class Consumable(Item):
	def __init__(self, weight = 0, damage = -1):
		super().__init__(weight)
		self.damage = damage

class BasicCreature:
	"base class for creatures"
	def __init__(self, max_health = 0,current_health = 0, base_attack = 0, base_defense = 0): # insert dictionary to populate with saved values (BasicCreature(**savedDict))
		self.max_health = max_health
		self.current_health = current_health
		self.base_attack = base_attack
		self.base_defense = base_defense
	def returnAsDict(self):
		return vars(self)
	def takeDamage(self, damage):
		self.current_health -= (damage - self.base_defense)
	def attackEnemy(self):
		return self.base_attack

class Player(BasicCreature):
	def __init__(self, max_health = 0,current_health = 0, base_attack = 0, base_defense = 0, weapon_slot = Weapon(), armor = {"Body" : None, "Head": None}):
		super().__init__(max_health ,current_health , base_attack, base_defense)
		self.weapon_slot = weapon_slot
		self.armor = armor
		self.calculateStats()
	def equipArmorPiece(self, armor_piece):
		if isinstance(armor_piece, Armor) and armor_piece.slot in self.armor:
			self.armor[armor_piece.slot] = armor_piece
	def calculateStats(self):
		#Armor
		self.armor_def = 0
		for i in self.armor:
			if isinstance(self.armor[i], Armor): 
				self.armor_def += self.armor[i].defense
		self.weapon_attack = 0
		if isinstance(self.weapon_slot, Weapon):
			self.weapon_attack += self.weapon_slot.attack
	def equipWeapon(self, weapon):
		if isinstance(weapon, Weapon):
			self.weapon_slot = weapon
	#Override
	def takeDamage(self, damage):
		self.current_health -= (damage - (self.base_defense + self.armor_def))
	#Override
	def returnAsDict(self):
		hilf = vars(self)
		if isinstance(hilf["weapon_slot"], Weapon):
			hilf["weapon_slot"] = vars(hilf["weapon_slot"])
		for i in self.armor:
			if isinstance(hilf["armor"][i], Armor): 
				hilf["armor"][i] = vars(hilf["armor"][i])
		return hilf
	#Override
	def attackEnemy(self):
		return (self.base_attack + self.weapon_attack)

class Fight:
	def __init__(self, party_1 = {}, party_2 = {}):
		self.party_1 = party_1
		self.party_2 = party_2
		self.turnCount = 0
		self.combat_log = ''''''
	def addPartyMember(self, member_name, new_member, party):
		if isinstance(new_member, BasicCreature):
			if party == 1:
				self.party_1[member_name] = new_member
			elif party == 2:
				self.party_2[member_name] = new_member
	def attackMember(self, attacking_side, party_1_member, party_2_member):
		if attacking_side == 1:
			self.party_2[party_2_member].takeDamage(self.party_1[party_1_member].attackEnemy())
			if self.party_2[party_2_member].current_health <= 0:
				del self.party_2[party_2_member]
		elif attacking_side == 2:
			self.party_1[party_1_member].takeDamage(self.party_2[party_2_member].attackEnemy())
			if self.party_1[party_1_member].current_health <= 0:
				del self.party_1[party_1_member]
		else:
			pass
	def isFightOver(self):
		if self.party_1 == {}:
			print("Party 1 lost")
			return True
		elif self.party_2 == {}:
			print("Party 2 lost")
			return True
		else:
			return False
	def saveFight(self):
		hilf = deepcopy(vars(self))
		for i in hilf["party_1"]:
			if isinstance(hilf["party_1"][i],BasicCreature):
				hilf["party_1"][i] = hilf["party_1"][i].returnAsDict()
			else:
				del hilf["party_1"][i]
		for i in hilf["party_2"]:
			if isinstance(hilf["party_2"][i],BasicCreature):
				hilf["party_2"][i] = hilf["party_2"][i].returnAsDict()
			else:
				del hilf["party_2"][i]
		with open("fightsavefile.txt", "w", encoding = 'utf-8') as file:
			json.dump(hilf, file, indent=4)