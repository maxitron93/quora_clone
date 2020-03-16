from rest_framework import serializers
from account.models import Account

class RegistrationSerializer(serializers.ModelSerializer):
    # Need to add this because password2 isn't in the Account model
    # So people can't read the password as it comes in
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}  # So people can't read the password as it comes in
        }

    # Override the save method so it only saves if the two password match
    def save(self):
        account = Account(
            email=self.validated_data['email']  # Validated data becomes available after a is_validated()
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # Check that passwords patch
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        # Create restrictions on password
        if len(password) < 8:
            raise serializers.ValidationError({'password': 'Password must be longer than 8 characters.'})
        else:
            account.set_password(password)  # Set the password
            account.save()  # Need to call .save() method
            return account  # Return the account
