from core.models import User, Role, Permission

def select_permissions():
    permissions = Permission.objects.all()
    print("\nAvailable permissions:")
    for index, permission in enumerate(permissions, start=1):
        print(f"{index}. {permission.name} (ID: {permission.id})")

    while True:
        choice = input("\nEnter the numbers of the permissions (comma separated): ").strip()
        if choice:
            try:
                selected_ids = [int(id.strip()) for id in choice.split(',')]
                selected_permissions = [permissions[id - 1] for id in selected_ids if 0 < id <= len(permissions)]
                if selected_permissions:
                    return selected_permissions
                else:
                    print("⚠️ No valid permissions selected. Try again.")
            except (ValueError, IndexError):
                print("⚠️ Invalid input. Try again.")

def add_one_admin_role():
    selected_permissions = select_permissions()

    role, created = Role.objects.update_or_create(
        code="admin_role",
        defaults={"name": "Admin Role"}
    )
    role.permissions.set(selected_permissions)

    if created:
        print(f"✅ Admin role created with permissions: {[perm.name for perm in selected_permissions]}")
    else:
        print(f"🔄 Admin role updated with permissions: {[perm.name for perm in selected_permissions]}")

def select_role():
    roles = Role.objects.all()
    print("\nAvailable roles:")
    for index, role in enumerate(roles, start=1):
        print(f"{index}. {role.name} (ID: {role.id})")

    while True:
        choice = input("\nEnter the number of the role to assign to the user: ").strip()
        if choice:
            try:
                role_id = int(choice)
                if 0 < role_id <= len(roles):
                    return roles[role_id - 1]
                else:
                    print("⚠️ Invalid role number. Try again.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a number.")

def add_one_admin_user():
    username = input("Enter username for the admin user: ").strip()
    email = input("Enter email for the admin user: ").strip()
    password = input("Enter password for the admin user: ").strip()
    selected_role = select_role()

    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.role = selected_role
    user.set_password(password)
    user.save()

    if created:
        print(f"✅ User {username} created with role {selected_role.name}")
    else:
        print(f"🔄 User {username} updated with role {selected_role.name}")

def run():
    print("Seeding admin role and user...")
    print("This will create an admin role and one admin user.")
    print("Select the options to execute...")
    while True:
        print("1. Add admin role with permissions")
        print("2. Add one admin user")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_one_admin_role()
        elif choice == "2":
            add_one_admin_user()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")