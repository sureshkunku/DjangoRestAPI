from rest_framework import serializers
from rest_app.models import Personal, Color
from django.contrib.auth.models import User, Group
from rest_framework import permissions, routers, serializers, viewsets


# first we define the serializers
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = '__all__' # ["username", "password", "email"]
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already taken")
        return data 

class ColorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Color
        fields = ["color_name"]


class PersonSerializer(serializers.ModelSerializer):
    
    color = ColorSerializer()
    
    class Meta:
        model = Personal
        fields = "__all__"
        # depth = 1 
    def validate(self, data):
        
        if data['age'] < 18:
            raise serializers.ValidationError("The given value is less than 18, please above 18")
        return data
    
    # def validate_age(self, age):
        
    #     if age < 18:
    #         raise serializers.ValidationError("The given value is less than 18, please above 18")
    #     return age