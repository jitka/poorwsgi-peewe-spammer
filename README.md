# poorwsgi-peewee-spammer

```
export MYSQL_HOST=127.0.0.1
export MYSQL_PASSWORD=$SECREAT
mysql> CREATE DATABASE spammer;
mysql> USE spammer;
mysql> CREATE TABLE mess (id INTEGER, next INTEGER, PRIMARY KEY (id));
python app/main.py
curl 127.0.0.1:8080/shuffle/<data_size>
curl 127.0.0.1:8080/walk/<random_number>/<sql_query_number>
```