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

    def get_current_inventory(self):
        '''
        This just returns the npc's current inventory
        :return: self.inventory_list
        '''

        return self.inventory_list

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
            exit(1)

        # Now let's add the item.
        self.inventory_list.append(item)

