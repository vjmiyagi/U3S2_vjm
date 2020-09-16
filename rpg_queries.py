import os
import sqlite3
import pandas as pd


# Connect to the sqlite database
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")
conn = sqlite3.connect(DB_FILEPATH)
curs = conn.cursor()


# This method runs a query and returns the results
def askme(query):
    r = curs.execute(query).fetchall()
    r = r[0]
    return r


print()


# How many total Characters are there?
q = """SELECT
            count(distinct character_id)
        FROM
            charactercreator_character;"""
r = askme(q)
t = "Total number of   characters are: "
print(t, r[0])


# How many of each specific subclass?
# CLERICS:
q = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_cleric;"""
r = askme(q)
t = "Total number of      clerics are:  "
print(t, r[0])


# FIGHTERS
q = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_fighter;"""
r = askme(q)
t = "Total number of     fighters are:  "
print(t, r[0])


# MAGES
q = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_mage;"""
r = askme(q)
t = "Total number of        mages are: "
print(t, r[0])


# NECROMANCER:
q = """SELECT
            count(distinct mage_ptr_id)
        FROM
            charactercreator_necromancer;"""
r = askme(q)
t = "Total number of necromancers are:  "
print(t, r[0])


# THIEF:
q = """SELECT
            count(distinct character_ptr_id)
        FROM
            charactercreator_thief;"""
r = askme(q)
t = "Total number of      thieves are:  "
print(t, r[0])


# ITEMS
q = """SELECT
            count(distinct item_id)
        FROM
            armory_item;"""
r = askme(q)
t = "Total number           items are: "
print(t, r[0])


# WEAPONS?
q = """SELECT
            count(distinct item_ptr_id)
        FROM
            armory_weapon;"""
r = askme(q)
t = "Total number         weapons are:  "
print(t, r[0])


# NON-WEAPONS:
q = """SELECT
            count(distinct item_id)
        FROM
            armory_item
        WHERE item_id < 138;"""
r = askme(q)
t = "Total number of  non-weapons are: "
print(t, r[0])
print()


# How many Items does each character have? (Return first 20 rows)
t = "Items carried by each character: "
q = """
    SELECT name as Name
    ,COUNT(item_id) as Items
    FROM charactercreator_character c, charactercreator_character_inventory i
    WHERE c.character_id = i.character_id
    GROUP BY c.character_id;"""
r = curs.execute(q).fetchmany(20)


df = pd.DataFrame(r, columns=["Character", "Items"])
print(df)
print()


# How many weapons does each character have? (Return first 20 rows)
t = "Weapons carried by each character: "
q = """
    SELECT name as Name
    ,COUNT(item_id) as Weapons
    FROM charactercreator_character c, charactercreator_character_inventory i
    WHERE c.character_id = i.character_id
    AND item_id > 137
    GROUP BY c.character_id;"""
r = curs.execute(q).fetchmany(20)
df = pd.DataFrame(r, columns=["Character", "Weapons"])
print(df)


# On average, how many items does each character have?
q = """
    SELECT
        count(DISTINCT item_id)
    FROM
        charactercreator_character_inventory
    Group BY
        character_id;"""
r = askme(q)
t = "The average # of   items per character carries is: "
print()
print(t, r[0])


# On average, how many weapons does each character have?
q = """
    SELECT
        count(DISTINCT item_id)
    FROM
        charactercreator_character_inventory
    WHERE
        item_id > 137
    Group BY
        character_id;"""
r = askme(q)
t = "The average # of weapons per character carries is: "
print(t, r[0])
print()


# Tidy up
curs.close()
conn.close()