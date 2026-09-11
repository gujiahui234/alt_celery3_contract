"""alt_celery3_contract: declarative, strongly-typed task contracts for alt_celery3.

This package is a pure *contract* layer: it declares the names, argument
signatures and Pydantic payload schemas of the Celery tasks served by the
``alt_celery3`` application — without carrying any of their business logic.

Typical imports::

    from alt_celery3_contract import TASK_CATALOG, TaskName
    from alt_celery3_contract.definitions import generate_many_students
    from alt_celery3_contract.schemas import GenerateManyStudentsPayload
"""

from __future__ import annotations

from .catalog import TASK_CATALOG, TaskContract
from .constants import TASK_EXAMPLE_ADD, TaskName
from .constants import (
    TASK_GENERATE_MANY_STUDENTS,
    TASK_GET_ONE_STUDENT,
    TASK_GET_UN_GROUPS,
    TASK_INIT_WEB_DB,
    TASK_SCHEDULED_ADD,
    TASK_SIMU_ADMISSION,
    TASK_SIMU_EXAM,
    TASK_SIMU_GRADUATE,
    TASK_SIMU_NCEE,
    TASK_TRY_MYSQL,
)
from .definitions import (
    add,
    generate_many_students,
    get_one_student,
    get_un_groups,
    init_web_db,
    scheduled_add,
    simu_admission,
    simu_exam,
    simu_graduate,
    simu_ncee,
    try_mysql,
)
from .schemas import (
    AddPayload,
    GenerateManyStudentsPayload,
    GetUnGroupsPayload,
    ScheduledAddPayload,
    SimuAdmissionPayload,
    SimuExamPayload,
    SimuGraduatePayload,
    SimuNceePayload,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # Catalog
    "TASK_CATALOG",
    "TaskContract",
    # Task names
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
    # Contract definitions
    "add",
    "scheduled_add",
    "try_mysql",
    "get_one_student",
    "generate_many_students",
    "init_web_db",
    "get_un_groups",
    "simu_ncee",
    "simu_admission",
    "simu_exam",
    "simu_graduate",
    # Payload schemas
    "AddPayload",
    "ScheduledAddPayload",
    "GenerateManyStudentsPayload",
    "GetUnGroupsPayload",
    "SimuNceePayload",
    "SimuAdmissionPayload",
    "SimuExamPayload",
    "SimuGraduatePayload",
]
