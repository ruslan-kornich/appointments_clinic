# appointments_clinic

# Rest API to manage user registration for clinic services

API Description:
- API for the manager, allows you to record a person for free time to a specific specialist.
- API for the administrator, allows you to create specialists, places and working hours for them.
- API for clients allows you to get a list of specialists, time and day of the appointment of a specialist.
## Stack:
Django/Django REST Framework, Python 

## Installation

-Clone repository

```bash
git clone https://github.com/ruslan-kornich/appointments_clinic.git
```

Create and activate virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install requirements:
```bash
$ pip install -r requirements.txt
```

Start server:

```bash
$ python manage.py runserver
```
## Distribution of rights from the admin panel:

Distribution of rights from the admin panel:

-Admin - is_superuser, is_staff.

-Manager - is_staff.

-Client - is_active.

Test Users url admin/ :
(login/password)
- admin/ admin
- manger/12345
- client/12345


Unregistered users and users with Client rights can only view the list of specialists and select the schedule of a specialist
## API Docs:

Authorization is based on a token JWT
```bash
/api/v1/workers/login/
```
Instead, you need to pass your username and password as a form data via POST request to this endpoint:
You'll get the tokens:
```bash
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2ODgwMjM5OCwiaWF0IjoxNjY4NzE1OTk4LCJqdGkiOiJlMDM0OGY3NmEzNTU0YzdiYWVjNTMzYjJhNzQ3OTU5MCIsInVzZXJfaWQiOjg1fQ.NEGeUd7bciv3YA2jK2ajNzbozxM51RI4Fq3ChR0-swc",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4ODAyMzk4LCJpYXQiOjE2Njg3MTU5OTgsImp0aSI6IjFkOTU4ZjJmN2MxYzQ0Nzk5ZTA4OGJmNGNkNjhkNWUyIiwidXNlcl9pZCI6ODV9.AsPi-s80rcS819RAIUoXqp4O17dRLpTRCetuBQPhATs"
}
```
## Intended data structure
### /api/v1/workers/
- GET - Availability data is available to all users

- POST  - Recording data only from the admin account
### /api/v1/workers/{id}
- PUT - Change data on request, available only to the admin
- DELETE  - Deleting an entry by ID


### /api/v1/clients/
- GET - List of clients

- POST  - Adding Clients
### /api/v1/clients/{id}
- PUT - Change data on request, available only to the admin
- DELETE  - Deleting an entry by ID

### /api/v1/appointments/
(CRUD for admin and managers)
- GET - List of appointments

- POST  - Adding appointments
### /api/v1/appointments/{id}
- PUT - Change data on request
- DELETE  - Deleting an entry by ID

The rest is the same CRUD for admin user
