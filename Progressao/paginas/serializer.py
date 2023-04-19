# from rest_framework import serializers
# from paginas.models import , Result

# class CampoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Campo
#         fields = ('DescriptionId','Description')

# class ResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Result
#         fields = 
from rest_framework import serializers
from paginas.models import User, PhraseUser, NL, Test

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PhraseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhraseUser
        fields = '__all__'

class NLSerializer(serializers.ModelSerializer):
    class Meta:
        model = NL
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'