from rest_framework import serializers
from .models import Announcement, Role, Department, User, Leave


class Departser(serializers.ModelSerializer):
    """
    部门自关联序列化
    """

    class Meta:
        model = Department
        fields = '__all__'


class Departmentser(serializers.ModelSerializer):
    """
    部门表序列化
    """
    parent = Departser()

    class Meta:
        model = Department
        fields = '__all__'


class Roleser(serializers.ModelSerializer):
    """
    角色表序列化
    """

    class Meta:
        model = Role
        fields = '__all__'


class Userser(serializers.ModelSerializer):
    """
    员工表序列化
    """
    department = Departmentser(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    roles = Roleser(many=True, read_only=True)
    roles_id = serializers.ListField(max_length=150, write_only=True)

    def create(self, data):
        id = data['roles_id']
        del data['roles_id']
        u = User.objects.create(**data)
        u.roles.add(*id)
        return u

    class Meta:
        model = User
        fields = '__all__'


class Update_Userser(serializers.ModelSerializer):
    """
    修改员工信息序列化器
    instance:数据库查出来的数据
    data :前台传过来数据
    """
    department_id = serializers.IntegerField(write_only=True)
    roles = Roleser(many=True, read_only=True)
    roles_id = serializers.ListField(write_only=True)

    def update(self, instance, data):
        d = data['roles_id']
        instance.name = data['name']
        instance.age = data['age']
        instance.gender = data['gender']
        instance.phone = data['phone']
        instance.address = data['address']
        instance.department_id = data['department_id']
        instance.position = data['position']
        instance.number = data['number']
        instance.image = data['image']
        instance.save()
        instance.roles.set(d)
        return instance

    class Meta:
        model = User
        fields = '__all__'


class Announcementser(serializers.ModelSerializer):
    """
    公告序列化和反序列化
    """

    user_id = serializers.IntegerField(write_only=True)
    user = Userser(read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'

    def create(self, data):
        user = Announcement.objects.create(**data)
        return user


class Leaveser(serializers.ModelSerializer):
    initiator = Userser(read_only=True)
    approve = Userser(read_only=True)
    leader = Userser(many=True, read_only=True)
    initiator_id = serializers.IntegerField(write_only=True)
    approve_id = serializers.IntegerField(write_only=True)
    leader_ids = serializers.CharField(max_length=100,write_only=True)

    def create(self, data):
        l = eval(data['leader_ids'])
        del data['leader_ids']
        le = Leave.objects.create(**data)
        le.leader.add(*l)
        return le

    class Meta:
        model = Leave
        fields = '__all__'
