from rest_framework import serializers
from .models import User, Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'code']


class RoleSerializer(serializers.ModelSerializer):
    # show permissions in response
    permissions = PermissionSerializer(many=True, read_only=True)
    # accept permission ids when creating/updating role
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Role
        fields = ["id", "name", "code", "is_employee", "permissions", "permission_ids"]

    def create(self, validated_data):
        permission_ids = validated_data.pop("permission_ids", [])
        role = Role.objects.create(**validated_data)
        role.permissions.set(permission_ids)
        return role

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop("permission_ids", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if permission_ids is not None:
            instance.permissions.set(permission_ids)
        return instance


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # show role details
    role_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)  

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_id', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        role_id = validated_data.pop('role_id', None)
        password = validated_data.pop("password")
        
        if role_id:
            try:
                role = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                raise serializers.ValidationError({"role_id": "Invalid role id"})
        validated_data['role'] = role if role_id else None
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        role_id = validated_data.pop('role_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if role_id == 0:
            instance.role = None
        elif role_id is not None:
            try:
                role = Role.objects.get(id=role_id)
                instance.role = role
            except Role.DoesNotExist:
                raise serializers.ValidationError({"role_id": "Invalid role id"})
        
        if password:
            instance.set_password(password)
        instance.save()
        return instance

