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

* Instructions to setup a CI/CD pipeline with Travis CI are present [here](https://medium.com/@soumoks/creating-a-django-ci-cd-pipeline-with-travis-ci-and-aws-elasticbeanstalk-b91bfedd144c)

