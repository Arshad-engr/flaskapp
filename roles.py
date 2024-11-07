# create_roles.py
from main import Role, User, db
from main import Migrate

def create_roles():
    admin = Role(id=1, name='Admin')
    editor = Role(id=2, name='Editor')
    writer = Role(id=3, name='Writer')
    db.session.add(admin)
    db.session.add(editor)
    db.session.add(writer)
    db.session.commit()
    print("Roles created successfully!")

# Function calling will create 4 roles as planned!
create_roles()