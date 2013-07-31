myvardump, myvardiff
============================

- myvardump.py: dump MySQL `show global variables` to json
- myvardiff.py: diff running MySQL `show global variables` to json(dumped by myvardump)

:: 

 $ python myvardump.py --config tmp/my.cnf --out tmp/test.json
 $ python myvardiff.py --config tmp/my.cnf --before tmp/test.json
 read_buffer_size:       131072 -> 1048576
 wait_timeout:   28890 -> 28800

Installation
============================
:: 

 git clone https://github.com/netmarkjp/myvardiff
 pip install MySQL-python

How to Use
============================
:: 

 python myvardump.py --config example.my.cnf --out variables.json

:: 

 python myvardiff.py --config example.my.cnf --before variables.json


Quick RUN
----------------------------

You can use ``<(printf 'CONFIG')`` instead of config file.

::

 python myvardump.py --config <(printf '[DEFAULT]\nhost=localhost\nuser=root\npassword=') --out tmp/test.json
 python myvardiff.py --config <(printf '[DEFAULT]\nhost=localhost\nuser=root\npassword=') --before tmp/test.json





Note
----------------------------
This program was inspired by myprofiler( https://github.com/methane/myprofiler )
