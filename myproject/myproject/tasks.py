from functools import wraps

from myproject.celeryconf import app
from .models import LetterDigit

from .utilities import get_lettercase_permutation


@app.task
def lettercase_permutation_task(job_id, string):
    job = LetterDigit.objects.get(id=job_id)
    job.status = 'started'
    job.save()
    try:
        job.result = get_lettercase_permutation(string)
        job.status = 'finished'
        job.save()
    except Exception as e:
        print('An error occured: ', str(e))
        job.result = None
        job.status = 'failed'
        job.save()
    return job.result
