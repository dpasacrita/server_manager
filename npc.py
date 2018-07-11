#!/usr/bin/python3.5

# Globals
# Max Inventory Size
MAX_INVENTORY = 20


class NPC:

    # Initialize NPC Object and register variables
    def __init__(self):

        # Base Values for Object
        # Bio
        self.name = ""
        self.race = ""
        self.age = ""
        # Stats
        self.strength = 1
        self.intelligence = 1
        self.agility = 1
        self.skill = 1
        # Condition
        self.health = 0
        self.damage = 0
        self.condition = "Healthy"
        self.status = "Uninjured"
        # Inventory/Equipment
        self.inventory_list = []
        self.active_weapon = {}
        self.active_armor = {}

    def calculate_health(self):
        '''
        This function calculates the health of the NPC.
        The health formula is defined by:
        strength*10

        :return:
        '''

        self.health = self.strength*10

    def set_initial_stats(self, stats):
        '''
        This function sets the npc's initial stats given a stat dictionary.
        Name and Race are required. The rest can use defaults but this is not recommended.

        :param stats:
        :return:
        '''

        # First check if the name and race are missing
        # If they're there, fill them in.
        if "name" not in stats:
            print("ERROR: 'health' value not in stats!")
            exit(1)
        else:
            self.name = stats["name"]
        if "race" not in stats:
            print("ERROR: 'race' value not in stats!")
            exit(1)
        else:
            self.race = stats["race"]

        # Now that we've checked that it's valid, lets fill in the stats.
        # Strength
        if "strength" in stats:
            self.strength = stats["strength"]
        else:
            print("WARN: 'strength' value not in stats. Using default of 1.")
        # Intelligence.
        if "intelligence" in stats:
            self.intelligence = stats["intelligence"]
        else:
            print("WARN: 'intelligence' value not in stats. Using default of 1.")
        # Agility
        if "agility" in stats:
            self.agility = stats["agility"]
        else:
            print("WARN: 'agility' value not in stats. Using default of 1.")
        # Skill
        if "skill" in stats:
            self.skill = stats["skill"]
        else:
            print("WARN: 'skill' value not in stats. Using default of 1.")

        # Calculate the NPCs Health
        self.calculate_health()

    def get_current_inventory(self):
        '''
        This just returns the npc's current inventory.

        :return: self.inventory_list
        '''

        return self.inventory_list

    def get_current_weapon(self):
        '''
        Returns the active weapon.

        :return: self.active_weapon
        '''

        return self.active_weapon

    def get_current_armor(self):
        '''
        Returns the active armor.

        :return: self.active_armor
        '''

        return self.active_armor

    def get_name(self):
        '''
        Returns the name.

        :return:
        '''

        return self.name

    def validate_item(self, item):
        '''
        Validates that a given item has all the necessary values.
        In theory works for all item types.

        :return:
        '''

        # If it's not even a dictionary just error there:
        if type(item) is not dict:
            print("ERROR: Item %s is not a dictionary. All items must be dictionaries." % item)
            return False
        # Make sure there's an "Item Type" variable. If not, error.
        if "item type" not in item:
            print("ERROR: Item %s has no item type variable." % item)
            return False

        # If the item is a sword, check some values
        if item["item type"] is "sword":
            # Make sure it has a valid range
            if "damage min" not in item:
                print("ERROR: Sword has no damage minimum!")
                return False
            if "damage max" not in item:
                print("ERROR: Sword has no damage maximum!")
                return False
            if item["damage min"] > item["damage max"]:
                print("ERROR: Sword's min damage is higher than maximum damage!")
                return False
            # If any of the values are negative error
            if item["damage min"] < 0 or item["damage max"] < 0:
                print("ERROR: Sword has negative damage values! Must be positive.")
                return False
            # Now let's check crit rate
            if "critical rate" not in item:
                print("ERROR: Sword has no critical rate!")
                return False
            # Make sure it's in from 0 to 100
            if item["critical rate"] < 0 or item["critical rate"] > 100:
                print("ERROR: Sword has an invalid Critical Rate. Must be from 0 to 100.")
                return False
            # Everything looks fine for the sword. Return True.
            return True

        # If the item is armor, check some other values
        elif item["item type"] is "armor":
            # Check to make sure it has an armor rating
            if "armor rating" not in item:
                print("ERROR: Armor has no armor rating!")
                return False
            # Gotta be a positive number
            if item["armor rating"] < 0:
                print("ERROR: Armor Rating must be a positive number.")
                return False
            # Everything looks fine, return True.
            return True

        # Lastly, if the item type is not currently verified, just return true.
        else:
            return True

    def inventory_add_item(self, item):
        '''
        Adds an item to the npc's inventory.
        Will fail if the npc's inventory is full.

        :param item:
        :return:
        '''

        # Check if the npc's inventory is full.
        # If so, return a failure.
        if len(self.inventory_list) >= MAX_INVENTORY:
            print("ERROR: Inventory is full! Cannot add item! You'll have to drop something.")
            return

        # Make sure it's a valid item.
        if not self.validate_item(item):
            print("ERROR: The item failed validation. Cannot add it.")
            return

        # Now let's add the item.
        self.inventory_list.append(item)

    def inventory_drop_item(self, item):
        '''
        Goes through the inventory list and drops the specified item.
        Will fail if the item does not exist.
        If there are two items with the same name, it will drop one.

        :param item:
        :return:
        '''

        # If the specified item is not in the inventory list, return an error.
        if item not in self.inventory_list:
            print("ERROR: Inventory List does not contain item %s!" % item)
            return
        else:
            self.inventory_list.remove(item)

    def equip_item(self, item):
        '''
        First thing this method does is determine if the item is a sword or armor.
        If it's not, no equipping for you. Error.
        Then it equips the item, replacing the currently equipped item if need be.

        :param item:
        :return:
        '''

        # If the specified item is not in the inventory list, return an error.
        if item not in self.inventory_list:
            print("ERROR: Inventory List does not contain item %s!" % item)
            return

        # We're going to re-validate the item first to make sure it's valid.
        if self.validate_item(item) is False:
            return

        # Now do one of three things.
        # If the item is a sword:
        if item["item type"] == "sword":
            self.active_weapon = item
            print("INFO: Made active weapon %s" % item)
        # If the item is armor:
        elif item["item type"] == "armor":
            self.active_armor = item
            print("INFO: Made active armor %s" % item)
        else:
            print("ERROR: Item Type is not sword or armor. Cannot Equip!")
            return
