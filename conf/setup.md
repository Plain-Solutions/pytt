PyTT
====

* install:
  * Ubuntu 14.04
  * `memecached` 1.4.14-0ubuntu9
  * `python` 2.7.6+
  * `mariaDB` 10.0.19+maria-1~trusty
  * latest `pip`
  * lastest `nginx`
* `pip install -r requirements.txt`
* set `binlog_format = MIXED` in `/etc/mysqld/my.cnf`
* restart `mysqld`
* `mysql -u root -pROOT_PASS < conf/db_adjustments/create_tt_database_and_user.sql`
* set your config properties in current directory in `config.properties` contents
  *  `[SSU]` section:
      * `ssu_user`
      * `ssu_password`
      * `ssu_url`
  * `[DB]` section:
     * `user`
     * `password`
     * `host`
	  * `port`
* `python manage.py migrate`
* `mysql -u YOUR_PYTT_USER -pYOUR_PYTT_PASS pytt < conf/db_adjustments/mariadb_adjustments.sql`
* `gunicorn -w 6 --bind 0.0.0.0:8000  pytt.wsgi:application`
* copy `nginx.conf` from `conf` directory to `/etc/nginx`
* restart nginx
* you are ready to go!

