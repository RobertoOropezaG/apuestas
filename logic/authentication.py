from repository.models import *

def save_login(token, profile):
    identity = Identity.query.filter_by(email=profile['email']).first()

    if not identity:
        return None

    identity.update_from_google(profile)

    if not identity.users:
        
        subscript = 1
        existing_user = User.query.filter_by(nick=identity.first_name).first()
        while existing_user:
            subscript += 1 
            existing_user = User.query.filter_by(nick=identity.first_name + str(subscript)).first()
        
        user = User(nick=identity.first_name + (str(subscript) if subscript > 1 else ''), token=token['access_token'])
        identity.users.append(user)
    else:
        user = identity.users[0]
        user.token = token['access_token']

    db.session.commit()

    return user


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user