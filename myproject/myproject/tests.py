import json
from rest_framework.test import APITestCase
from .models import UserBirthday



class LetterDigitAPI(APITestCase):
    """ Test module for the contact LetterDigit API """
    def test_can_generate_correct_result(self):
        url = '/letter_digits/'
        res = self.client.post(url, {'string': 'ab'})
        self.assertEqual(str(json.loads(res.content)['result']), "['ab', 'aB', 'Ab', 'AB']")

        res = self.client.post(url, {'string': '1a2'})
        self.assertEqual(str(json.loads(res.content)['result']), "['1a2', '1A2']")


class UserBirthdayAPI(APITestCase):
    """ Test module for the contact UserBirthday API """

    def setUp(self):
        self.valid_json = """
            [ {"first_name": "Eike", "last_name": "Bartels", "email": "bar@dsf.de", "birthday": "01.03.1989"}, 
              {"first_name": "Anthony", "last_name": "Ngene", "email": "montaro@g.com", "birthday": "08.05.1993"} ]
        """
        self.create_two_user_birthdays()

    def create_two_user_birthdays(self):
        url = '/user_birthdays/'
        res = self.client.post(url, {'json': self.valid_json})
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),  {"status": "completed", "issues": []}
        )

    def test_can_save_user_birthdays(self):
        self.assertEqual(len(UserBirthday.objects.all()), 2)

    def test_does_not_save_invalid_user_data(self):
        url = '/user_birthdays/'
        json = """
            [ {"first_name": "Eike", "email": "bar@dsf.de", "birthday": "01.03.1989"}]
        """
        res = self.client.post(url, {'json': json})
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {"status": "completed with issues.", "issues": [
                {"data": {"first_name": "Eike", "email": "bar@dsf.de", "birthday": "01.03.1989"},
                 "errors": ["Missing last_name", "Email already exist."]}]}
        )

    def test_can_filter_by_date(self):
        url = '/user_birthdays/'
        res = self.client.get(url)
        self.assertEqual(len(json.loads(res.content)), 2)

        res = self.client.get(url + '?from=1990-03-02&to=1994-02-20')
        self.assertEqual(len(json.loads(res.content)), 1)

class AverageAge(APITestCase):
    """ Test module for the contact  AverageAge API """

    def setUp(self):
        self.valid_json = """
            [ {"first_name": "Eike", "last_name": "Bartels", "email": "bar@dsf.de", "birthday": "01.03.1989"}, 
              {"first_name": "Anthony", "last_name": "Ngene", "email": "montaro@g.com", "birthday": "08.05.1993"} ]
        """
        url = '/user_birthdays/'
        self.client.post(url, {'json': self.valid_json})

    def test_computes_correct_average(self):
        url = '/user_birthdays/average/'
        res = self.client.get(url)
        print(res.content)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'), {"average_age": 28.5}
        )
