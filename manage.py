from flask_script import Manager
from comic import app, db, Author, Comic

manager = Manager(app)


@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    DC = Author(name='DC', about='DC is a comic publisher that owns the Justice League, known as being dark.')
    Marvel = Author(name='Marvel', about='Marvel is a comic publisher that owns avengers and is known for being family friendly.')
    DarkHorse = Author(name='Dark Horse', about='Dark House is a lesser known comic publisher.')
    comic1 = Comic(name='Deathstroke', year=1980, lyrics="Mercenary considered an antihero with enhanced abilities", author=DC)
    comic2 = Comic(name='Deadpool', year=1991, lyrics="Psychotic mercenary capable of breaking the 4th wall and considered immortal. Antihero.", author=Marvel)
    comic3 = Comic(name='Hellboy', year=1993  , lyrics="A devil like character with enhanced abilities who is hated, but still fights for good", author=DarkHorse)
    db.session.add(DC)
    db.session.add(Marvel)
    db.session.add(DarkHorse)
    db.session.add(comic1)
    db.session.add(comic2)
    db.session.add(comic3)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
