pytt
====

[SSU TimeTables](http://vk.com/ssutt) is a project maintained by Plain Solutions, group of several students, which is created to bring university schedules to your palm - your mobile devices.

General
======

<table border="0"><tr><td><img src="logo.png" /></td><td> <b>pytt</b> is a new backend server for the project. It's written in Python and intended to be faster, simpler and better than its predecessor, which was faithfully serving us for a year. </td></tr></table>

Project is a typical API-orientated web application written in Django, which uses `gunicorn` for load balancing, `nginx` for security and `MariaDB` as database backend, because I love seals (and it's quite a fast and a good solution).

REST API completed with Django REST Framework, which is quite a mess, but still a good solution.

Let's look through main files:

* `models.py` – description of models
* `urls.py` - descirption of all available requests
* `serializers.py` - JSON serialisation module
* `views.py` – core logic here 
* `parse.py` – incoming data parsing (from XML)
* `fetch.py` – downloading module

Also, there are a few Django commands under `pytt/management/commands/`, mainly for maintenance/initial setup:

* `create_pr.py` – caluclate parities of weeks and save them to the DB. Should be run with `cron` each 1st September
* `create_tr.py` – create table of time references: correlation between class index and actual time for each differing department
* `reset_index.py` – `Model.objects.all().delete()` doesn't reset indices, so this command runs `ALTER` query on all the required tables.
* `update_tt.py` – command, which atomically drops previous DB and fills it once again. Should be run with `cron` according to desired frequency of updates.

Other desicrptions are available on the project wiki. 

How to run
==========

First, please check, that you executed all the steps of Setup article.

Pytt is intended to run with Gunicorn behind nginx. Sample `nginx.conf` can be found on Wiki page and in `conf` directory of the repo. 

Then, you should run `gunicorn -w NUMBER_OF_WORKERS --bind 0.0.0.0:8000  pytt.wsgi:application` from the root of the repo and restart `nginx`. 

Dependencies
============

* Any Linux system, preferably Ubuntu/Debian
* Python 2.7.x
* MariaDB 10.0.x
* memcached 1.4
* Python libraries requirements are listed in `requirements.txt` for simpler installation via `pip`:
	* Django 1.7.5
	* djangorestframework 3.1.3
	* requests 2.2.1
	* mysql-connector-python 2.0.4
	* python-memcached 1.54
	* gunicorn 19.3.0
	* httpretty 0.8.10 (for tests only) 

	
License
=======

BSD

Authors
=======

Vlad Slepukhin ([vk](vk.com/vladfau), [linkedin](https://www.linkedin.com/profile/view?id=373710624))

Acknowledgements
===========

* Alexey Kornev
* Vadim Kiselev



