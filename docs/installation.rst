********************
Installation & Setup
********************

Installation
============

For the moment, the project is in beta mode with no releases. To install you
will need to use the ``--editable`` option of pip ::

    pip install -e https://github.com/jibaku/places.git#egg=places

Or you can go to `the github page <https://github.com/jibaku/places>`_ to
checkout the project and run ``python setup.py install``.

Setup
=====

.. highlight:: python

1. Add ``places`` to your ``settings.INSTALLED_APPS``.
2. Sync the database::

    python manage.py syncdb
