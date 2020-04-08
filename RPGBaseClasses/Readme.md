# RPG Base Classes #
#### Version 0.1 ####

- base classes that allow creation of a basic rpg
- Basic Creatures and Player
- Items (Armor, Weapons, Consumables)
- Spells (not implemented yet)

## Example: ##
```python
# create a beast and a player
beast = BasicCreature(3,3,1,0)
player = Player(5,5,1,0)
# let the player equip a weapon and armor
player.equipWeapon(Weapon(0,1))
player.equipArmorPiece(Armor(0,1))
# initilize a fight and add the player and the beast
fight = Fight()
fight.addPartyMember("player",player,1)
fight.addPartyMember("beast",beast,2)
# save the fight in a file
fight.saveFight()
# the fight loop
while not fight.isFightOver():
	print("Player Health:", fight.party_1["player"].current_health)
	print("Beast Health:", fight.party_2["beast"].current_health)
	# the player attacks the beast
	fight.attackMember(1,"player","beast")
# load the saved fight
with open("fightsavefile.txt", "r", encoding = 'utf-8') as file:
	x = json.load(file)
y = Fight(**x)
# print party 2 of the loaded fight
print(y.party_2)
```