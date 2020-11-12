from django.contrib.auth import  get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import  serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # I gonna ad "extra keywordsarg"--> what it dose ? it allows us to configure a few extra settings
        # in our model serializer. 
        # for what i gonna use this for? to insure that password write only and minimum is 5 charecter 
        extra_kwargs = {"password": {"write_only":True, "min_length": 5}}

    # over write create function here.
    def create(self, validated_data):
        """Create a new user with a encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # with the pop function you mast apply default value.
        # what it does? it it very simaller to get, after it's retrieved it 
        # it will remove it from original dictionary.
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user 


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        # removes whitespace 
        trim_whitespace = False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user 
        return attrs
