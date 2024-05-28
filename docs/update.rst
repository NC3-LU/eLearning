Updating the application
========================

Run update bash script
-----------------------

All you have to do is:

``<install_path>`` for exemple : ``/home/<user>/eLearning``

.. code-block:: bash

    $ cd <install_path>
    $ bash scripts/update.sh -a

Usage: ``bash scripts/update.sh --help``

.. code-block:: bash

    $ bash scripts/update.sh --help
    Usage: scripts/update.sh [options]
    Options:
    -u, --update-repositories   Update git repositories
    -npm, --update-npm-packages Update npm packages
    -p, --update-python-packages Update python packages
    -m, --migrate-database      Migrate database
    -c, --compile-translations  Compile translations
    -s, --collect-static        Collect static files
    -a, --update-all            Update all components
    --help                      Display this help message


Or manually
--------

.. code-block:: bash

    $ cd <install_path>/theme/
    $ git pull origin master
    $ cd ..
    $ git pull origin master
    $ npm install
    $ poetry install
    $ poetry shell
    $ python manage.py migrate
    $ python manage.py compilemessages
    $ python manage.py collectstatic


Restart Apache server
---------------------

Finally, restart Apache:

.. code-block:: bash

    $ sudo systemctl restart apache2.service
