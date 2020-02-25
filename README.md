# URL-shortner

A client server web application build using python-flask micro-framework and MySQL at backend.
Long URL is stored at new index in database. Shortened URL is returned to the user by doing base-62
encoding on the index of stored long URL. Original URL is retrieved using base-62 decoding on the
shortened URL.

Since the shortened URL can be 8 characters Long, hence it can serve upto 62^7 = 317 trillion unique queries. 

Editor used: Sublime text 3.

Requirements :
Python 2.7+
flask
Mysql
