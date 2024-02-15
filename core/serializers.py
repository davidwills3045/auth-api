from rest_framework import serializers
from django.contrib.auth.models import User

class Userserializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','username','password','email']