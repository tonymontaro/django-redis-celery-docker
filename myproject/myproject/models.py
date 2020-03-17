from datetime import datetime
from django.db import models

from .utilities import count_alphas, get_lettercase_permutation


class LetterDigit(models.Model):
    STATUSES = (
        ('pending', 'pending'),
        ('started', 'started'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )

    status = models.CharField(choices=STATUSES, max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    string = models.TextField()
    result = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Generate lettercase permutation before saving result to the database.
        If the number of alphabets is less the 20, then it can be computed in less than a second, compute synchronously.
        If it's greater than 20, then run the task in the background with celery, the user can query again with the
        provided url to check if the process is complete.
        """
        super(LetterDigit, self).save(*args, **kwargs)
        if self.status == 'pending':
            alphas = count_alphas(self.string)
            if alphas < 20:
                self.result = get_lettercase_permutation(self.string)
                self.status = 'finished'
                self.save()
            elif alphas > 27:
                raise Exception("This will generate more 260 million different permutations. Please don't crash my server.")
            else:
                from .tasks import lettercase_permutation_task
                lettercase_permutation_task.delay(job_id=self.id, string=self.string)


class UserBirthday(models.Model):
    email = models.CharField(max_length=255, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    birthday = models.DateField(null=False)
    age = models.IntegerField()

    def save(self, *args, **kwargs):
        """
        Calculate user's age before saving to the DB.
        """
        self.calculate_age()
        super(UserBirthday, self).save(*args, **kwargs)

    def calculate_age(self):
        birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
        today = datetime.today()
        self.age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
