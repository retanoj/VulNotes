# coding:utf-8

from app import create_app, db
from app.models import VulRecord, VulType
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, VulRecord=VulRecord, VulType=VulType)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def dev():
    app.run(port=8001, debug=True)


@manager.command
def prod():
    app.run(port=8001, debug=False)


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import VulType, VulRecord
    upgrade()

    VulType.data_init()
    VulRecord.data_init()


if __name__ == '__main__':
    manager.run()
