from core.models import Permission

def add_permissions():
    # Create permissions
    perms = {
        "create_user": "Can create user",
        "view_all_users": "Can view all users",
        "view_employees_only": "Can view employees only",
        "update_user": "Can update user",
        "delete_user": "Can delete user",
        "manage_roles": "Can manage roles & permissions",
    }

    perm_objs = {}
    for code, name in perms.items():
        Permission.objects.get_or_create(code=code, defaults={"name": name})

    print(f"✅ Roles & permissions seeded successfully")

def run():
    add_permissions()
