from repository.models import *

def save_login(token, profile):
    identity = Identity.query.filter_by(email=profile['email']).first()

    if not identity:
        return None

    identity.update_from_google(profile)

    if not identity.users:
        user = User(nick=identity.first_name, token=token['access_token'])
        identity.users.append(user)
    else:
        user = identity.users[0]
        user.token = token['access_token']

    db.session.commit()

    return user


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user