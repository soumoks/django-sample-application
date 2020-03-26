### django-sample-application                                          [![Build Status](https://travis-ci.org/soumoks/django-sample-application.svg?branch=master)](https://travis-ci.org/soumoks/django-sample-application)

![alt text](https://i.imgur.com/AiveVw6.png)
* Clone the repository

```
git clone https://github.com/soumoks/django-sample-application.git
```

* Create a virtualenv
```
python -m venv <name_of_virtualenv>
```

* Activate the virtualenv
(Windows only)
```
<name_of_virtualenv>\Scripts\activate.bat
```

* Install the dependencies
```
pip install -r requirements.txt
```

* Setup ElasticBeanstalk
```
eb init -p python-3.6 django-tutorial
eb init
eb create django-env
```
* [Add a database to your EB environment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.db.html)

* Deploy the application
```
eb deploy
```
* Add the relevant environment variables to your environment. These variables are required to establish a connection with the database
```
import os
os.environ['RDS_DB_NAME'] = ""
os.environ['RDS_USERNAME'] = ""
os.environ['RDS_PASSWORD'] = ""
os.environ['RDS_HOSTNAME'] = ""
os.environ['RDS_PORT'] = ""
```
These variables depend on the database used. The above variables are required for AWS RDS

* Run the application
```
python manage.py runserver
```

* Instructions to setup a CI/CD pipeline with Travis CI are present [here](https://medium.com/@soumoks/creating-a-django-ci-cd-pipeline-with-travis-ci-and-aws-elasticbeanstalk-b91bfedd144c)

