from random import randint, choice as rc

from faker import Faker
from app import app
from models import db, Hero, Power, HeroPower

fake = Faker()
strengths = ["Strong", "Weak", "Average"]
super_names = ["Ms. Marvel",
               "Squirrel Girl",
               "Spider_Gwen",
               "The Wasp",
               "Scarlet Witch",
               "Captain Marvel",
               "Dark Phoenix",
               "Storm",
               "ShadowCat",
               "Elektra"]

with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()

    heroes = []
    for i in range(10):
        hero = Hero(name=fake.name(), super_name=super_names[i],)
        heroes.append(hero)

    db.session.add_all(heroes)

    power_names = ["super strength",
                   "flight",
                   "super human senses",
                   "elasticity",
                ]
    power_desc = [
       "gives the wielder super-human strengths",
       "gives the wielder the ability to fly through the skies at supersonic speed",
       "allows the wielder to use her senses at a super-human level",
       "can stretch the human body to extreme lengths"
       ]
    powers = []
    for i in range(len(power_names)):
        power = Power(name=power_names[i], description=power_desc[i],)
        powers.append(power)

    db.session.add_all(powers)

    hero_powers = []
    for super_hero in heroes:
        for i in range(randint(1, 10)):
            strength = rc(strengths)
            power_instance = rc(powers)
            hp = HeroPower(strength=strength, hero=super_hero, power=power_instance)
            hero_powers.append(hp)
    db.session.add_all(hero_powers)

    db.session.commit()


