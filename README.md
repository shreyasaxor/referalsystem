**Referal System**

this application is built to signup users  and refer others to earn
 referal credits which is built with Django Rest Framework
 
 **How to run**

`$ virtualenv project-env`   
`$ source project-env/bin/activate `  
`$ pip install -r requirements.txt  `   
`$ cd projectname/`      
`$ python manage.py makemigrations`   
`$ python manage.py migrate` 
`$ python manage.py runserver`

**API Detail**

To get all users list   

`GET:http://127.0.0.1:8000/usermgmt/api/`

-------------------------------------------------------
To save user(self signup)

`POST:http://127.0.0.1:8000/usermgmt/api/`   

Request body

{

        "email": "emaial@cms.com",
        "first_name": "john",
        "password": 12345678        
}

-----------------------------------------------------

To save user with referalcode

`POST:http://127.0.0.1:8000/usermgmt/api/121212323`   

Request body

{

        "email": "emaial@cms.com",
        "first_name": "john",
        "password": 12345678        
}

---------------------------------------------------------

To authenticate user and get referal,total-earned

`POST:http://127.0.0.1:8000/usermgmt/api/121212323`   

Request body

{

        "email": "emaial@cms.com",
        "password": 12345678        
}
