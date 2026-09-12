"""Canonical task-name constants of the alt_celery3 contract package.

The values below are the *global registration names* used by the Celery
application of ``alt_celery3``. They are the single source of truth for any
producer, worker or scheduler that needs to address a task by name
(``celery_app.send_task(name, ...)`` / beat schedules / monitoring).

Producers should reference :class:`TaskName` (or the module-level aliases)
instead of hard-coding raw strings so a rename on the worker side can be
detected by static analysis and by the compatibility verifier script.
"""

from __future__ import annotations

from enum import Enum


class TaskName(str, Enum):
    """Registered Celery task names of ``alt_celery3``.

    The members are ``str`` subclasses, so they can be used directly wherever
    Celery expects a plain string task name.
    """

    #: Sum of two integers (getting-started example).
    TASK_EXAMPLE_ADD = "tasks.example.add"
    #: Periodic counterpart of the addition example (dispatched by beat).
    TASK_SCHEDULED_ADD = "tasks.scheduled.add"
    #: Connectivity probe of the MySQL ``web_db`` database.
    TASK_TRY_MYSQL = "tasks.db.try_mysql"
    #: Generate one simulated student and persist it.
    TASK_GET_ONE_STUDENT = "tasks.db.get_one_student"
    #: Threaded, million-scale bulk student generation.
    TASK_GENERATE_MANY_STUDENTS = "tasks.db.generate_many_students"
    #: Destructive rebuild of ``web_db`` / ``log_db`` and the business tables.
    TASK_INIT_WEB_DB = "tasks.db.init_web_db"
    #: LLM-driven university + major-group collection (SiliconFlow API).
    TASK_GET_UN_GROUPS = "tasks.ai.get_un_groups"
    #: Simulated college entrance exam (高考) for one year.
    TASK_SIMU_NCEE = "tasks.simu.ncee"
    #: Tier-based university admission of an exam cohort.
    TASK_SIMU_ADMISSION = "tasks.simu.admission"
    #: In-university exam simulation for an academic year.
    TASK_SIMU_EXAM = "tasks.simu.exam"
    #: Graduation with GPA computation for a cohort enrolled 4 years earlier.
    TASK_SIMU_GRADUATE = "tasks.simu.graduate"
    #: One-stop pipeline: ncee -> admission -> exams -> graduation for a cohort.
    TASK_ONE_STOP_GRADUATION = "tasks.pipeline.one_stop_graduation"


# --- Module-level aliases ----------------------------------------------------
# These mirror the ``TASK_*`` constants of ``app.config`` in alt_celery3 so
# both projects can share one import path without any mapping boilerplate.

TASK_EXAMPLE_ADD = TaskName.TASK_EXAMPLE_ADD.value
TASK_SCHEDULED_ADD = TaskName.TASK_SCHEDULED_ADD.value
TASK_TRY_MYSQL = TaskName.TASK_TRY_MYSQL.value
TASK_GET_ONE_STUDENT = TaskName.TASK_GET_ONE_STUDENT.value
TASK_GENERATE_MANY_STUDENTS = TaskName.TASK_GENERATE_MANY_STUDENTS.value
TASK_INIT_WEB_DB = TaskName.TASK_INIT_WEB_DB.value
TASK_GET_UN_GROUPS = TaskName.TASK_GET_UN_GROUPS.value
TASK_SIMU_NCEE = TaskName.TASK_SIMU_NCEE.value
TASK_SIMU_ADMISSION = TaskName.TASK_SIMU_ADMISSION.value
TASK_SIMU_EXAM = TaskName.TASK_SIMU_EXAM.value
TASK_SIMU_GRADUATE = TaskName.TASK_SIMU_GRADUATE.value
TASK_ONE_STOP_GRADUATION = TaskName.TASK_ONE_STOP_GRADUATION.value

__all__ = [
    "TaskName",
    "TASK_EXAMPLE_ADD",
    "TASK_SCHEDULED_ADD",
    "TASK_TRY_MYSQL",
    "TASK_GET_ONE_STUDENT",
    "TASK_GENERATE_MANY_STUDENTS",
    "TASK_INIT_WEB_DB",
    "TASK_GET_UN_GROUPS",
    "TASK_SIMU_NCEE",
    "TASK_SIMU_ADMISSION",
    "TASK_SIMU_EXAM",
    "TASK_SIMU_GRADUATE",
    "TASK_ONE_STOP_GRADUATION",
]
