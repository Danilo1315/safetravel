from rest_framework import serializers
from django.contrib.auth.models import User
from user_app.models import Account

class RegistrationSerializer(serializers.ModelSerializer):
    # Definimos password de confirmacion
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password2', 'name']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'Invalid password'})
        
        if Account.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email existing'})
        
        # account = Account(email=self.validated_data['email'], username = self.validated_data['username'])
        account = Account.objects.create_user(
            name=self.validated_data['name'],
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        
        account.set_password = self.validated_data['password']
        # account.set_password(password)
        account.save()
        
        return account