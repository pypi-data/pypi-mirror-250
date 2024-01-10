
.. image:: https://readthedocs.org/projects/abstract-tracker/badge/?version=latest
    :target: https://abstract-tracker.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/abstract_tracker-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/abstract_tracker-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/abstract_tracker-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/abstract_tracker-project

.. image:: https://img.shields.io/pypi/v/abstract-tracker.svg
    :target: https://pypi.python.org/pypi/abstract-tracker

.. image:: https://img.shields.io/pypi/l/abstract-tracker.svg
    :target: https://pypi.python.org/pypi/abstract-tracker

.. image:: https://img.shields.io/pypi/pyversions/abstract-tracker.svg
    :target: https://pypi.python.org/pypi/abstract-tracker

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/abstract_tracker-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/abstract_tracker-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://abstract-tracker.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://abstract-tracker.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/abstract_tracker-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/abstract_tracker-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/abstract_tracker-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/abstract-tracker#files


Welcome to ``abstract_tracker`` Documentation
==============================================================================
📔 See `Full Documentation HERE <https://abstract-tracker.readthedocs.io/en/latest/>`_.

.. image:: https://abstract-tracker.readthedocs.io/en/latest/_static/abstract_tracker-logo.png
    :target: https://abstract-tracker.readthedocs.io/en/latest/

This library help you track the business critical task status moving from ``pending`` (todo), to ``in_progress``, then possibly to ``failed`` (also with error traceback information) or ``succeeded``. If it failed too many times, it will be marked as ``exhausted``. If you never want to see it anymore, it will be marked as ``ignored``.

This library provides the abstraction layer that can work with arbitrary backend. For instance, local file, AWS S3, SQL Database, AWS DynamoDB, Redis, MongoDB, ..., as you wish.


.. _install:

Install
------------------------------------------------------------------------------

``abstract_tracker`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install abstract-tracker

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade abstract-tracker
