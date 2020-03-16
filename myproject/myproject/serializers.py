from rest_framework import serializers

from .models import LetterDigit, UserBirthday


class LetterDigitSerializer(serializers.HyperlinkedModelSerializer):
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        return (obj.result[:200] + '...') if (obj.result and len(obj.result) > 200) else obj.result

    class Meta:
        model = LetterDigit
        extra_kwargs = {
            name: {'read_only': True} for name in ['result', 'status']
        }


class UserBirthdaySerializer(serializers.ModelSerializer):
    json = serializers.CharField(max_length=None, write_only=True)

    class Meta:
        model = UserBirthday
        extra_kwargs = {
            name: {'read_only': True} for name in ['email', 'first_name', 'last_name', 'birthday', 'age']
        }
