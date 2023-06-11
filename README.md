# Bookshop

This repository is a container platform for the sale of books, consisting of several services.
The main idea of ​​this project is to use a separate store API to update information about books and their quantity, process orders and order statuses in it.
The store service sends requests to the API in order to: periodically synchronize information about books, create new orders, periodically synchronize information about the status of customer orders.
Customers also receive email notifications after: submitting an order, changing the status of an order in the API.
API requests and email sending are handled by the Celery service.

## Stack:

- Django (To create a Shop website)
- Django Rest Framework (To create a Store API)
- Docker (To make many microservices work together)
- PostgreSQL (To store data for Shop and Store)
- Nginx (To forward client's requests to right web applications: Shop port 8000, Store port 8001, Mailhog port 8025)
- Celery (To perform time-intensive tasks for shop, as described above)
- RabbitMQ (To receive tasks for celery)
- Redis (To save celery tasks results)
- Bootstrap (To make my shop service look awesome)
- jQuery, AJAX (To increment and decrement items in cart without reloading the page)
- MailHog (To simulate email sending)
- Flake8 (To maintain the backend code readable)
- Debug Toolbar (To help in database queries optimization)

## Installation:

1. Install and run docker on your computer.
2. Clone this repository.
3. Create a .env file in backend/shop and fill it with many random letters and numbers for SECRET_KEY variable and an empty string for TOKEN. For example:
   ```.env
   SECRET_KEY="tnc4tuo4n5yg4vw5ygc4wgmwrgiqgyr8guwerugh7w68gh45ugmrwhg"
   TOKEN=""
   ```
4. Create a .env file in backend/store and fill it with many random letters and numbers for SECRET_KEY. For example:
   ```.env
   SECRET_KEY="c7ty4678wvnghwgw4gyrt5grbgutr8gh84hw8jg8w4g9tgwb9r9g"
   ```
5. Open terminal in root folder (Bookshop) and run:
   ```shell
   docker-compose -f docker/docker-compose.yml build
   docker-compose -f docker/docker-compose.yml up
   ```
   Wait a bit until terminal logs stop.
   This will be our terminal window in which the project is running. DON'T CLOSE IT UNTIL MY PROJECT IS IN USE.
   P.S.: If "docker-compose" not working, try writing like this: "docker compose"

6. Finally, we can access our shop service: localhost:8000, store service: localhost:8001, mailhog: localhost:8025
7. This is not all. Now let's add some books to our store. But at first we need to create an admin user for store. Open a new terminal window in the root folder and write these commands:
    ```shell
   docker-compose -f docker/docker-compose.yml exec store bash
   ```
   ```python
   python manage.py createsuperuser
   ```
   You will have to enter what shell is asking. Do not exit this terminal window.
8. In this step let's create and save admin's token in order shop can send requests to store which will create orders in it. Run these commands:
   ```shell
   python manage.py shell
   ```
   ```python
   from django.contrib.auth import get_user_model
   from rest_framework.authtoken.models import Token
   User = get_user_model()
   admin_user = User.objects.get(username='')
   token = Token.objects.create(user=admin_user)
   token.key
   ```
   Then copy the key which was printed out (WITHOUT THE QUOTES) and paste it into backend/shop/.env file into TOKEN variable quotes. Close this terminal window.
9. Open a new terminal window in the root folder. Now we are creating a shop admin:
    ```shell
   docker-compose -f docker/docker-compose.yml exec shop bash
   ```
   ```python
   python manage.py createsuperuser
   ```
   You will have to enter what shell is asking.
10. Finally, you are ready to go to localhost:8001/admin and to finally create some books.
11. You are welcome to return to localhost:8000 to test my project further.
12. To stop the project just press CMD+C (CTRL+C) and wait until all containers stop.
13. To rerun the project go to the project root folder and paste this command:
   ```shell
   docker-compose -f docker/docker-compose.yml up
   ```
   All data will be the same as in the previous sessions!