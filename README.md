# `Data Includer`

API service for working with csv files and data visualization. Users have tokenized access to the api.

___

## *Project Status*

***Completed &#10003;***
___
## Functionality
- API for CRUD operations with dataset via [DRF + Django ORM](https://github.com/Segfaul/data_includer/blob/365c4244e5efc07e8d0f03606ec423c37fc326dd/data_includer/api/views.py#L15-L151)
- Authorization and validation/error handling
- Basic dataset operations via Django generic view classes and [AJAX](https://github.com/Segfaul/data_includer/blob/365c4244e5efc07e8d0f03606ec423c37fc326dd/data_includer/table/static/dataset/js/ajax.js#L43) requests
- [Documentation](https://github.com/Segfaul/data_includer/blob/365c4244e5efc07e8d0f03606ec423c37fc326dd/data_includer/data_includer/urls.py#L28) and writing [tests](https://github.com/Segfaul/data_includer/blob/365c4244e5efc07e8d0f03606ec423c37fc326dd/data_includer/api/tests/test.py#L11-L115) of the service's main API

## Technologies and Frameworks
- Python 3.10
- Django 4.2.3
- DRF 3.14.0
- Pandas
- PostgreSQL
- Swagger, Docker
___

## Installation

1. Clone the repository to the local machine

    ```shell
    git clone https://github.com/Segfaul/data_includer.git
    ```

2. Go to the repository directory

    ```shell
    cd data_includer
    ```

3. Create and activate a virtual environment

    ```shell
    python -m venv env
    source env/bin/activate
    ```

4. Set project dependencies

    ```shell
    pip install -r requirements.txt
    ```

5. Move to the project directory

    ```shell
    cd data_includer
    ```

6. Configure the configuration file .env

    ```shell
    nano .env
    ```

7. Create database migrations and apply them

    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```

8. Create a Django project superuser (admin)

    ```python
    python manage.py createsuperuser
    ```

9. Run the project on localhost in the background

    ```python
    python manage.py runserver &
    ```

10. Go to the site and enter the previously created data of the superuser (step 8)

    ```shell
    http://127.0.0.1:8000
    ```

11. In the future you can deploy the project on a remote server

    ```python
    python manage.py runserver 123.123.123.123:8000 &
    ```

12. In case of a problem, the program will stop automatically or you can stop execution using

    ```shell
    ps aux | grep ".py"
    kill PID
    ```

13. Also you can build a docker app and run the container

    ```shell
    docker build -t app .
    docker run -d app
    ```

___

## API endpoints
- **[DELETE]** */api/delete/{file_id}/?api_token=...* - delete csv file on server related to user's api_token
- **[GET]** */api/generate_token/* - generates api_token for an authorized user
- **[GET]** */api/revoke_token/* - revokes api_token for an authorized user
- **[GET]** */api/read/?api_token=...* - read csv file using get request and pandas dataframe as a response
- **[GET]** */api/list/?api_token=...* - list of csv files on server related to user's api_token
- **[POST]** */api/upload/?api_token=...* - upload csv file on server related to user's api_token
___
