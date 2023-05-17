def is_admin(current_user):
    print(current_user.role_id, "role")
    if current_user.role_id == 1:
        print("not admin")
        return False
    return True


def is_maintainer(current_user):
    if current_user.role_id != 3:
        return False
    return True
