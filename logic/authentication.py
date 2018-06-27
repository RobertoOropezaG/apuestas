from repository.models import *
from flask_login import current_user
from pprint import pprint

def save_login(token, profile):
    identity = Identity.query.filter_by(email=profile['email']).first()

    if not identity:
        return None

    identity.update_from_google(profile)

    if not identity.users:
        # get an available nick name
        subscript = 1
        existing_user = User.query.filter_by(nick=identity.first_name).first()
        while existing_user:
            subscript += 1 
            existing_user = User.query.filter_by(nick=identity.first_name + str(subscript)).first()
        
        #create new user
        user = User(nick=identity.first_name + (str(subscript) if subscript > 1 else ''), token=token['access_token'])
        identity.users.append(user)
    else:
        user = identity.users[0]
        user.token = token['access_token']

    db.session.commit()

    return user


def get_user_by_signature(signature):
    user_id = signature
    can_be_admin = False

    if User.includes_admin_signature(signature):
        can_be_admin = True
        user_id = User.get_id_from_admin_signature(signature)

    user = User.query.get(user_id)
    if can_be_admin:
        if not user.can_be_admin:
            #tried to authenticate as admin without having that priviledge
            return None

        user.logged_as_admin = True

    return user


def authenticate_admin_password(admin_password):
    if not current_user.can_be_admin:
        return False, "Current user can't be an admin"

    if current_user.logged_as_admin:
        return False, "User is already logged as admin"
    
    if not current_user.matches_admin_password(admin_password):
        return False, "Wrong password"

    current_user.logged_as_admin = True

    return current_user, None


def logout_admin():
    if not current_user.can_be_admin:
        return False, "Current user can't be an admin"

    if not current_user.logged_as_admin:
        return False, "User is not logged as admin"

    current_user.logged_as_admin = False

    return current_user, None

