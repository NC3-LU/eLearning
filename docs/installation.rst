Installation
============

This section covers the installation steps of the sofware.

System packages
---------------

.. code-block:: bash

    $ sudo apt install gettext curl npm

Poetry
------

.. code-block:: bash

    $ curl -sSL https://install.python-poetry.org | python3 -


at the end of the `~/.bashrc` file add the line:

.. code-block:: bash

    $ export PATH="/root/.local/bin:$PATH"


PostgreSQL
----------
Install PostgreSQL, the version provided by default for your
GNU/Linux distribution.

.. code-block:: bash

    $ sudo apt-get install postgresql


Create a database, database user:

.. code-block:: bash

    $ sudo -u postgres createuser <username>
    $ sudo -u postgres createdb <database>
    $ sudo -u postgres psql
    psql (15.6 (Debian 15.6-0+deb12u1))
    Type "help" for help.
    postgres=# alter user <username> with encrypted password '<password>';
    ALTER ROLE
    postgres=# grant all privileges on database <database> to <username>;
    GRANT
    postgres=#


E-Learning Platform
----------------------------------------------------------------

.. code-block:: bash

    git clone https://github.com/NC3-LU/eLearning.git
    cd eLearning
    npm install


Copy the config and adjust the DB connection and the other settings:

.. code-block:: bash

    cp elearning/config_dev.py elearning/config.py
    poetry install
    poetry shell
    python manage.py migrate
    python manage.py collectstatic
    poetry manage.py compilemessagess


Theme
`````

In this case, the theme (static and templates) of the sofware will be cloned into the ``theme`` folder.
You can replace it by your own. Currently one theme is available:

- https://github.com/NC3-LU/eLearning_daaz_theme  (default theme, DAAZ Theme)

Exemple:

.. code-block:: bash

    cd eLearning
    git clone https://github.com/NC3-LU/eLearning_daaz_theme theme



Configuration
`````````````

In the configuration file ``elearning/config.py`` , ensures that you have configured:

- ``PUBLIC_URL``
- ``ALLOWED_HOSTS``
- ``SITE_NAME``
- ``DATABASES``
- ``HASH_KEY`` and ``SECRET_KEY``
- ``DEBUG``: must be set to ``False`` in a production environment
- etc.

You **must really** set **your** secret keys.

Here is an example for the Fernet hash key (``HASH_KEY``):

.. code-block:: bash

    $ python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key())'
    b'Xaj5lFGAPiy2Ovzi4YmlWh-s4HHikFV4AswilOPPYN8='


For the Django secret key (``SECRET_KEY``), you can for example do:

.. code-block:: bash

    $ python -c 'import secrets; print(secrets.token_hex())'
    9cf5c7b13e469e6f6a9403b33410589031cfe927df6471a1cbdef1d4deb57c37


Launch the Django application
-----------------------------

.. code-block:: bash

    poetry run python manage.py runserver 127.0.0.1:8000

Of course, do not do that for a production environment.


Apache
------

The ``mod_wsgi`` package provides an Apache module that implements a WSGI compliant
interface for hosting Python based web applications on top of the Apache web
server. Install Apache and this module.


.. code-block:: bash

        $ sudo apt install apache2 libapache2-mod-wsgi-py3


.. note::

    Only in the case you can not use the version of mod_wsgi from your
    GNU/Linux distribution:

    .. code-block:: bash

        $ sudo apt install apache2 apache2-dev # apxs2
        $ wget https://github.com/GrahamDumpleton/mod_wsgi/archive/refs/tags/5.0.0.tar.gz
        $ tar -xzvf 5.0.0.tar.gz
        $ cd mod_wsgi-5.0.0/
        $ ./configure --with-apxs=/usr/bin/apxs2 --with-python=/home/<user>/.pyenv/shims/python
        $ make
        $ sudo make install


    Then in ``/etc/apache2/apache2.conf`` add the lines:

    .. code-block:: bash

        LoadFile /home/<user>/.pyenv/versions/3.11.0/lib/libpython3.11.so
        LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so


    Restart Apache:

    .. code-block:: bash

        sudo systemctl restart apache2.service



For the next steps you must have a valid domain name.


Example of VirtualHost configuration file
`````````````````````````````````````````

Modify the ``<install_path>``, ``<user>``, ``<virtualenv_path>`` tags as appropriate

For <virtualenv_path> check using :

.. code-block:: bash

    $ cd <install_path>
    $ poetry env info


.. code-block:: apacheconf

    <VirtualHost *:80>
        ServerAdmin info@nc3.lu
        ServerName elearning.nc3.lu
        DocumentRoot /var/www/html
        RewriteEngine on
        RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
    </VirtualHost>

    <VirtualHost *:80>
        ServerAdmin info@nc3.lu
        ServerName elearning.nc3.lu
        DocumentRoot <install_path>
        WSGIDaemonProcess elearning python-path=<install_path> python-home=<virtualenv_path>/lib/python3.10/site-packages/
        WSGIProcessGroup elearning
        WSGIScriptAlias / <install_path>/elearning/wsgi.py

        <Directory "<install_path>/elearning/">
            <Files "wsgi.py">
                Require all granted
            </Files>
            WSGIApplicationGroup %{GLOBAL}
            WSGIPassAuthorization On

            Options Indexes FollowSymLinks
            Require all granted
        </Directory>

        Alias /static <install_path>/elearning/static
        <Directory <install_path>/static>
            Require all granted
        </Directory>

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/elearning.nc3.lu_access.log combined
        ErrorLog ${APACHE_LOG_DIR}/elearning.nc3.lu_error.log

        # Let's Encrypt configuration
        SSLCertificateFile /etc/letsencrypt/live/elearning.nc3.lu/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/elearning.nc3.lu/privkey.pem
        Include /etc/letsencrypt/options-ssl-apache.conf
    </VirtualHost>


Then configure HTTPS properly. If you want to use Let's Encrypt:

.. code-block:: bash

    sudo apt install certbot python3-certbot-apache
    sudo certbot certonly --standalone -d elearning.nc3.lu
    sudo a2enmod rewrite
    sudo systemctl restart apache2.service

Verify that the certificate will be automatically updated:

.. code-block:: bash

    $ cat /etc/letsencrypt/renewal/elearning.nc3.lu.conf
    # Options used in the renewal process
    [renewalparams]
    account = <-account-id->
    authenticator = apache
    server = https://acme-v02.api.letsencrypt.org/directory
