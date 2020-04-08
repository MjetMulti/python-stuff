from copy import deepcopy
import json

MAX_CHOICES = 10 # 0 -9

class Spell: # NOT USABLE
	def __init__(self):
		self.name = None
		self.mana_cost = 0
		self.type = "void"
		self.damage = 0

class Item:
	def __init__(self, weight = 0, name = None):
		self.weight = weight
		self.name = name

class Weapon(Item):
	def __init__(self, weight = 0, name = "Hands", attack = 1):
		super().__init__(weight, name)
		self.attack = attack

class Armor(Item):
	def __init__(self, weight = 0, name = None, defense = 0, slot = "Body"):
		super().__init__(weight, name)
		self.defense = defense
		self.slot = slot

class Consumable(Item):
	def __init__(self, weight = 0, name = None, damage = -1):
		super().__init__(weight, name)
		self.damage = damage

class BasicCreature:
	def __init__(self, max_health = 0,current_health = 0, base_attack = 0, base_defense = 0): # insert dictionary to populate with saved values (BasicCreature(**savedDict))
		self.max_health = max_health
		self.current_health = current_health
		self.base_attack = base_attack
		self.base_defense = base_defense

	def returnAsDict(self):
		return vars(self)

	def takeDamage(self, damage):
		self.current_health -= max(damage - self.base_defense, 0)

	def attackEnemy(self):
		return self.base_attack

	def onTurn(self):
		pass

	def onFightStart(self):
		pass

	def onFightEnd(self):
		pass

class Player(BasicCreature):
	class_lookup = {
		"Weapon": Weapon,
		"Armor": Armor,
		"Consumable": Consumable,
		"Spell": Spell,
		"Item": Item
	}
	def __init__(self,
				max_health = 0,
				current_health = 0,
				base_attack = 0,
				base_defense = 0,
				weapon_slot = Weapon(),
				armor = {"Body" : None, "Head": None},
				bag = {"Weapon": [], "Armor": [], "Consumable": []},
				max_mana = 0,
				current_mana = 0,
				mana_regen = 0,
				spells = {},
				gold = 0,
				**kwargs # to absorb additional arguments that are not needed as they get generated later => maybe use later
				):
		super().__init__(max_health ,current_health , base_attack, base_defense)
		self.weapon_slot = weapon_slot
		self.armor = armor
		self.bag = bag
		self.max_mana = max_mana
		self.current_mana = current_mana
		self.mana_regen = mana_regen
		self.spells = spells
		self.gold = gold
		self.calculateStats()
		self.establishActions()

	def earnGold(self, gold):
		self.gold += gold

	def looseGold(self, gold):
		self.gold -= gold
	
	def buyItem(self, cost, item_to_buy):
		if isinstance(item_to_buy, Item) and self.putItemInBag(item_to_buy):
			self.gold -= cost
			return True
		else:
			return False

	def establishActions(self):
		self.actions = []
		if isinstance(self.weapon_slot, Weapon):
			self.actions.append("attack")
		if len(self.spells) > 0:
			self.actions.append("spell")
		hilf = [len(self.bag[i]) > 0 for i in self.bag]
		if True in hilf:
			self.actions.append("bag")

	def calculateStats(self):
		#Armor
		self.armor_def = 0
		for i in self.armor:
			if isinstance(self.armor[i], Armor): 
				self.armor_def += self.armor[i].defense
		#Weapon
		self.weapon_attack = 0
		if isinstance(self.weapon_slot, Weapon):
			self.weapon_attack += self.weapon_slot.attack

	def equipArmorPiece(self, armor_piece):
		if isinstance(armor_piece, Armor) and armor_piece.slot in self.armor:
			self.armor[armor_piece.slot] = armor_piece
			return True
		else:
			return False

	def equipWeapon(self, weapon):
		if isinstance(weapon, Weapon):
			self.weapon_slot = weapon
			return True
		else:
			return False
	
	def putItemInBag(self, obj):
		for i in self.bag:
			if isinstance(obj,self.class_lookup[i]):
				self.bag[i].append(obj)
				return True
		return False

	def takeItemFromBag(self, item_type, idx):
		try:
			return self.bag[item_type].pop(idx)
		except:
			return False

	def castSpell(self, spell):
		if isinstance(spell, Spell) and spell.mana_cost <= self.current_mana:
			self.current_mana -= spell.mana_cost
			return True # Maybe return damage/damage_type later to implement buffs or abilities
		else:
			return False

	#Override
	def takeDamage(self, damage):
		self.current_health -= max(damage - (self.base_defense + self.armor_def), 0)

	#Override
	def returnAsDict(self):
		hilf = deepcopy(vars(self))
		# Weapon
		if isinstance(hilf["weapon_slot"], Weapon):
			hilf["weapon_slot"] = vars(hilf["weapon_slot"])
		# Armor
		for i in hilf["armor"]:
			if isinstance(hilf["armor"][i], Armor): 
				hilf["armor"][i] = vars(hilf["armor"][i])
		# Bag
		for i in hilf["bag"]:
			for j in range(len(hilf["bag"][i])):
				if isinstance(hilf["bag"][i][j], Item):
					hilf["bag"][i][j] = vars(hilf["bag"][i][j])
		return hilf

	#Override
	def attackEnemy(self):
		return (self.base_attack + self.weapon_attack)

	#Override
	def onTurn(self):
		self.current_mana = min(self.max_mana, self.current_mana + self.mana_regen)

class Fight:
	class_lookup = {
		"BasicCreature": BasicCreature,
		"Player": Player
	}
	def __init__(self, party_1 = {}, party_2 = {}, turn_count = 0, combat_log = ''''''):
		self.party_1 = party_1
		self.party_2 = party_2
		self.turn_count = turn_count
		self.combat_log = combat_log
		if self.party_1 != {}:
			for i in self.party_1:
				self.addPartyMember(i, self.class_lookup[self.party_1[i][0]](**(self.party_1[i][1])),1)
			for i in self.party_2:
				self.addPartyMember(i, self.class_lookup[self.party_2[i][0]](**(self.party_2[i][1])),2)

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
			if isinstance(hilf["party_1"][i],BasicCreature): # only save creatures
				if isinstance(hilf["party_1"][i],  Player):
					hilf["party_1"][i] = ["Player",hilf["party_1"][i].returnAsDict()]
				else:
					hilf["party_1"][i] = ["BasicCreature",hilf["party_1"][i].returnAsDict()]
			else:
				del hilf["party_1"][i]
		for i in hilf["party_2"]:
			if isinstance(hilf["party_2"][i],BasicCreature):
				if isinstance(hilf["party_2"][i],  Player):
					hilf["party_2"][i] = ["Player",hilf["party_2"][i].returnAsDict()]
				else:
					hilf["party_2"][i] = ["BasicCreature",hilf["party_2"][i].returnAsDict()]
			else:
				del hilf["party_2"][i]
		with open("fightsavefile.txt", "w", encoding = 'utf-8') as file:
			json.dump(hilf, file, indent=4)

beast = BasicCreature(3,3,1,0)
player = Player(5,5,1,0)
player.equipWeapon(Weapon(0,1))
player.equipArmorPiece(Armor(0,1))
player.earnGold(10)
player.buyItem(3, Armor())
fight = Fight()
fight.addPartyMember("player",player,1)
fight.addPartyMember("beast",beast,2)
