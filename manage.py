from flask_script import Manager
from comics import app, db, Company, Character

manager = Manager(app)


# reset the database and create some initial data
@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    DC = Company(name='DC', about='DC is a company that produces comics or movies based on superheros. Known for being very dark.')
    Marvel = Company(name='Marvel', about='Marvel is a family-friendly company that produces comics and movies that are very lighthearted.')
    character1 = Character(name='Deathstroke', year=2000, about="DC mercenary considered an antihero who's typically involved with Batman.", company=DC)
    character2 = Character(name='Deadpool', year=2014, about="Mercenary considered an antihero who's immortal and can break the 4th wall.", company=Marvel)
    db.session.add(DC)
    db.session.add(Marvel)
    db.session.add(character1)
    db.session.add(character2)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
