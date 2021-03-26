from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()#This get the user model class
        fields = ('email', 'password', 'name')#This are fields that will be accessible to the api to read or write
        #These are fields that we are going to accept when we are creating users. If u added a new user field, you
        #can just add it the fields
        extra_kwargs = {'password':{'write_only': True, 'min_length':5}}#This ensures that the password is write only
        #and the minimum length allowed for the password is 5

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)#This imports create user model in models.py

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    #The authenticaton serializer by default accepts only username and password, but we are modifying it to accept
    #email

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False#the django restframework serializer will trim of the white space, so by equating white trim_whitespace
        #the django restframe work wont remove the white space

    )

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')#if he is not a user and the api is called, the msg meaning message
            #needs to be displayed, the msg is passed below
            raise serializers.ValidationError(msg, code='authentication')#and then this an error is raised

        attrs['user'] = user
        return attrs
