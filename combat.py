#!/usr/bin/python3.5
import random

# Globals
BASE_DAMAGE = 1
UNARMED_DAMAGE = 1
CRITICAL_MULTIPLIER = 2


def calculate_weapon_damage(char1):
    '''
    Calculate the damage that char1 will do against something
    This is determined by rolling for how much damage char1 does based on their weapon.

    :param char1: Damage Dealer
    :return: damage: The damage we've done.
    '''

    # Start with base damage.
    damage = BASE_DAMAGE

    # First determine if char1 has a weapon
    if bool(char1.get_current_weapon()) is False:
        print("COMBAT: %s has no weapon. Damage set to 1." % char1.get_name())
        damage = UNARMED_DAMAGE
        return damage
    # They have a weapon, so let's grab it.
    try:
        weapon = char1.get_current_weapon()
    except Exception as e:
        print("ERROR: %s" % e)
        print("ERROR: Failed to get current weapon, even though char1 should have one.")
        return damage

    rolled_damage = roll_damage(weapon)
    final_damage = calculate_critical(weapon, rolled_damage)
    print("COMBAT: " + char1.get_name() + " rolled %s damage." % final_damage)

    return final_damage


def roll_damage(weapon):
    '''
    Rolls for a random number in between the weapon's minimum and maximum.

    :param weapon: The Weapon we're working with here.
    :return: damage: random number in between min and max.
    '''
    # Start with Base damage:
    damage = BASE_DAMAGE

    # Now let's calculate the damage.
    try:
        minimum = weapon["damage min"]
    except Exception as e:
        print("ERROR: %s" % e)
        print("ERROR: Failed to get weapon's minumum damage. Perhaps something went wrong with validation?")
        return damage
    try:
        maximum = weapon["damage max"]
    except Exception as e:
        print("ERROR: %s" % e)
        print("ERROR: Failed to get weapon's maximum damage. Perhaps something went wrong with validation?")
        return damage
    # Now get a number between those.
    try:
        rolled_damage = random.randint(minimum, maximum)
        return rolled_damage
    except Exception as e:
        print("ERROR: %s" % e)
        print("ERROR: Couldn't roll damage. Minimum and Maximum possible invalid.")
        return damage


def calculate_critical(weapon, rolled_damage):

    # Use the rolled damage as a base.
    final_damage = rolled_damage

    # Grab the weapon's critical rate:
    try:
        crit_rate = weapon["critical rate"]
    except Exception as e:
        print("ERROR: %s" % e)
        print("ERROR: Failed to get weapon's critical rate. Perhaps something went wrong with validation?")
        return final_damage

    # Now let's calculate the critical.
    # We'll roll a number between 1 and 100.
    # If the number is less than or equal to the crit rate, it criticals.
    critical = random.randint(1, 100)
    # If we succeeded, double damage.
    if critical <= crit_rate:
        print("COMBAT: CRITICAL HIT!")
        final_damage = rolled_damage * CRITICAL_MULTIPLIER
        return final_damage
    else:
        return final_damage
