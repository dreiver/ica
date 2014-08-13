This file is for you to describe the ica application. Typically
you would include information such as the information below:

Installation and Setup
======================

Install ``ica`` using easy_install::

    $ easy_install ica

Make a config file as follows::

    $ paster make-config ica config.ini

Tweak the config file as appropriate and then setup the application::

    $ paster setup-app config.ini

Then you are ready to go.

Installation:

    # Dependences for python debian/ubuntu support
    $ aptitude install python-pip python-virtualenv python-dev
    $ cd /home
    $ virtualenv env
    $ source env/bin/activate
    $ cd ica/
    $ pip install -r requirements.txt
    $ pip install -r rdbms.txt
    # Adjust custom configuration
    $ editor development.ini
    $ python setup.py develop

Run:

    $ paster serve --reload development.ini

Run gunicorn:

    $ gunicorn --paste production.ini -c ica/config/gunicorn.conf.py

Run gunicorn with external event lib

    $ gunicorn --paste production.ini -k gevent -c ica/config/gunicorn.conf.py
