.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add DynamoDB backend support, based on the `pynamodb_mate <https://github.com/MacHu-GWU/pynamodb_mate-project/blob/master/examples/patterns/status-tracker.ipynb>`_ project)
- Add Redis backend support.

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.1 (2024-01-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the base classes for all trackers.
- Add the ``FileTracker``, ``S3Tracker``
- Add the following public API:
    - ``abstract_tracker.api.logger``
    - ``abstract_tracker.api.TaskLockedError``
    - ``abstract_tracker.api.NoMoreRetryError``
    - ``abstract_tracker.api.TaskExhaustedError``
    - ``abstract_tracker.api.TaskIgnoredError``
    - ``abstract_tracker.api.StatusEnum``
    - ``abstract_tracker.api.T_STATUS_ENUM``
    - ``abstract_tracker.api.T_ID``
    - ``abstract_tracker.api.BaseTracker``
    - ``abstract_tracker.api.T_TRACKER``
    - ``abstract_tracker.api.FileTracker``
    - ``abstract_tracker.api.S3Tracker``
