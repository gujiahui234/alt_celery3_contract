alt_celery3_contract
====================

Declarative, strongly-typed **task contracts** for the ``alt_celery3``
Celery application.

The package scans nothing at runtime; it is a generated, static snapshot of
every Celery task served by ``alt_celery3``:

- canonical task names (``constants`` / :class:`~alt_celery3_contract.TaskName`),
- argument signatures as pure ``NotImplementedError`` stubs (``definitions``),
- Pydantic payload schemas with declared validation constraints (``schemas``),
- a global ``TASK_CATALOG`` mapping names to contracts and schemas.

Contents
--------

.. toctree::
   :maxdepth: 2

   api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
