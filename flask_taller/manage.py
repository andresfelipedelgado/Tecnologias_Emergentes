# manage.py


from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#hay que cambiarlo
from project.server import app, db, models, api

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

@manager.command
def run_app():
    app.run(debug=True)


if __name__ == '__main__':
    manager.run()
