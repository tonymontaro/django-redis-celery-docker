import json
from datetime import datetime
from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from django.core.cache import cache
from django.db.models import Avg


from .serializers import LetterDigitSerializer, UserBirthdaySerializer
from .models import LetterDigit, UserBirthday
from rest_framework.response import Response

class LetterDigitViewSet(
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    Letter Digit API
    GET /letter_digits/ - lists stored results
    POST /letter_digits/ data={string: abC} - processes the string and returns a result
    GET /letter_digits/id - get result by Id
    """
    queryset = LetterDigit.objects.all()
    serializer_class = LetterDigitSerializer

    def post(self, request):
        string = request.data.get('string').lower()
        result_from_cache = cache.get(string)
        if result_from_cache:
            return Response(result_from_cache)

        result = self.get_from_db_or_generate(string, request)
        cache_res = dict(result)
        del cache_res['url']
        cache.set(string, cache_res, None)
        return Response(result)

    def get_from_db_or_generate(self, string, request):
        result = LetterDigit.objects.filter(string=string)
        if result:
            result = result[0]
        else:
            result = LetterDigit(string=string)
            result.save()
        result = LetterDigitSerializer(result, context={'request': request})
        data = result.data
        return data


class UserBirthdayViewSet(
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    User Birthday API
    GET /user_birthdays/ - lists stored results from the database
    POST /user_birthdays/ data={json: [...]} - processes the json and saves valid items to DB
    GET /user_birthdays/id - get result by Id
    """
    queryset = UserBirthday.objects.all()
    serializer_class = UserBirthdaySerializer

    def list(self, request):
        from_query = request.GET.get('from', '1970-01-01')
        to_query = request.GET.get('to', datetime.today().strftime('%Y-%m-%d'))
        try:
            birthdays = UserBirthday.objects.filter(birthday__gte=from_query, birthday__lte=to_query)
        except Exception as e:
            return Response({'error': 'Invalid date formate. It must be in YYYY-MM-DD format.'})
        serializer = UserBirthdaySerializer(birthdays, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            data = json.loads(request.data.get('json'))
        except:
            return Response({'status': 'incomplete', 'issues': ['Invalid Json']})
        issues = []
        for item in data:
            validation = self.validate_data(item)
            if validation['is_valid']:
                day, month, year = item['birthday'].split('.')
                item['birthday'] = '-'.join([year, month, day])
                try:
                    result = UserBirthday(**item)
                    result.save()
                except Exception as e:
                    issues.append({'data': item, 'errors': [str(e)]})
            else:
                issues.append({'data': item, 'errors': validation['errors']})
        update_average_age_cache()
        status = "completed with issues." if issues else "completed"
        return Response({'status': status, 'issues': issues})

    def validate_data(self, item):
        errors = []
        for required in ['email', 'first_name', 'last_name', 'birthday']:
            if not item.get(required, ''):
                errors.append(f'Missing {required}')
        if 'email' in item and UserBirthday.objects.filter(email=item['email']):
            errors.append('Email already exist.')
        return {'is_valid': True} if not errors else {'is_valid': False, 'errors': errors}


class AverageAge(APIView):
    """
    AverageAge API
    GET /user_birthdays/average/ - returns average age from cache or computes/store it in cache if it did not exist.
    """
    def get(self, request):
        average = cache.get('__average_age', version=2)
        if average is None:
            average = update_average_age_cache()
        return Response({'average_age': average})


def update_average_age_cache():
    average = UserBirthday.objects.all().aggregate(Avg('age'))['age__avg']
    cache.set('__average_age', round(average, 2), None, version=2)
    return average
