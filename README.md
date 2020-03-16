## User Birthday and LetterCase Permutation app

### API Endpoints

#### Letter Digit

* **GET /letter_digits/** (lists stored Letter Digit permutation results)
* **POST /letter_digits/** (data={string: abC}, processes the string and returns a result)
* **GET /letter_digits/id** (get result by Id)


#### User Birthday


* **GET /user_birthdays/** (lists stored user birthday results from the database)
* **GET /user_birthdays/?from=1990-03-02&to=1994-02-20** (filter stored user birthdays results based on start/end date)
* **POST /user_birthdays/** (data={json: [...]} - processes the json and saves valid items to DB)
* **GET /user_birthdays/id/** (get result by Id)

* **GET /user_birthdays/average/** (returns average age from cache or computes/store it in cache if it did not exist.)

### Install 

    docker-compose build

### Usage

    docker-compose up
    
- visit: http://127.0.0.1:8000/

- Letter Digit API: **http://127.0.0.1:8000/letter_digits/**

- User Birthday API: **http://127.0.0.1:8000/user_birthdays/**


### Credits

- For bootstraping the project: https://blog.syncano.rocks/configuring-running-django-celery-docker-containers-pt-1/  by Justyna Edyta Ilczuk
