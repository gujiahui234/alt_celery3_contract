"""Global task catalog mapping task names to contract functions and schemas.

:py:data:`TASK_CATALOG` is the single lookup table that ties a canonical
Celery task name to:

- its declarative contract function (see :mod:`.definitions`),
- its optional Pydantic payload schema (see :mod:`.schemas`),
- the source module of the implementation inside ``alt_celery3``,
- whether the source task is declared with ``bind=True``.

Producers can use the catalog to validate call payloads *before* dispatching
them over the broker; tooling can use it to generate clients or docs.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from . import constants, definitions, schemas


@dataclass(frozen=True, slots=True)
class TaskContract:
    """Static contract record of one Celery task.

    Attributes:
        name: Canonical task registration name (e.g. ``tasks.example.add``).
        definition: Declarative contract function (signature mirror only).
        schema: Pydantic payload model, or ``None`` for zero-argument tasks.
        module: Source module of the implementation inside ``alt_celery3``.
        bound: Whether the source task is declared with ``bind=True`` (its
            leading ``self`` argument is stripped from the contract).
    """

    name: str
    definition: Callable[..., Any]
    schema: type[BaseModel] | None
    module: str
    bound: bool

    def validate_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """Validate producer keyword arguments against the payload schema.

        Args:
            kwargs: Keyword arguments intended for the task.

        Returns:
            The validated (and defaulted) keyword arguments.

        Raises:
            pydantic.ValidationError: When the payload schema rejects the
                arguments, or when the task expects a schema and none is
                given but arguments were supplied.
        """
        if self.schema is None:
            if kwargs:
                raise ValueError(
                    f"Task {self.name!r} takes no arguments, got: "
                    f"{sorted(kwargs)!r}"
                )
            return {}
        model = self.schema.model_validate(kwargs)
        return dict(model.model_dump(mode="json", exclude_none=False))


#: Every task of ``alt_celery3``, keyed by canonical task name.
TASK_CATALOG: dict[str, TaskContract] = {
    constants.TASK_EXAMPLE_ADD: TaskContract(
        name=constants.TASK_EXAMPLE_ADD,
        definition=definitions.add,
        schema=schemas.AddPayload,
        module="app.tasks.example_tasks",
        bound=False,
    ),
    constants.TASK_SCHEDULED_ADD: TaskContract(
        name=constants.TASK_SCHEDULED_ADD,
        definition=definitions.scheduled_add,
        schema=schemas.ScheduledAddPayload,
        module="app.tasks.scheduled_tasks",
        bound=True,
    ),
    constants.TASK_TRY_MYSQL: TaskContract(
        name=constants.TASK_TRY_MYSQL,
        definition=definitions.try_mysql,
        schema=None,
        module="app.tasks.db_tasks",
        bound=False,
    ),
    constants.TASK_GET_ONE_STUDENT: TaskContract(
        name=constants.TASK_GET_ONE_STUDENT,
        definition=definitions.get_one_student,
        schema=None,
        module="app.tasks.db_tasks",
        bound=False,
    ),
    constants.TASK_GENERATE_MANY_STUDENTS: TaskContract(
        name=constants.TASK_GENERATE_MANY_STUDENTS,
        definition=definitions.generate_many_students,
        schema=schemas.GenerateManyStudentsPayload,
        module="app.tasks.bulk_student_tasks",
        bound=True,
    ),
    constants.TASK_INIT_WEB_DB: TaskContract(
        name=constants.TASK_INIT_WEB_DB,
        definition=definitions.init_web_db,
        schema=None,
        module="app.tasks.init_db_tasks",
        bound=False,
    ),
    constants.TASK_GET_UN_GROUPS: TaskContract(
        name=constants.TASK_GET_UN_GROUPS,
        definition=definitions.get_un_groups,
        schema=schemas.GetUnGroupsPayload,
        module="app.tasks.ai_tasks",
        bound=True,
    ),
    constants.TASK_SIMU_NCEE: TaskContract(
        name=constants.TASK_SIMU_NCEE,
        definition=definitions.simu_ncee,
        schema=schemas.SimuNceePayload,
        module="app.tasks.simulation_tasks",
        bound=True,
    ),
    constants.TASK_SIMU_ADMISSION: TaskContract(
        name=constants.TASK_SIMU_ADMISSION,
        definition=definitions.simu_admission,
        schema=schemas.SimuAdmissionPayload,
        module="app.tasks.simulation_tasks",
        bound=True,
    ),
    constants.TASK_SIMU_EXAM: TaskContract(
        name=constants.TASK_SIMU_EXAM,
        definition=definitions.simu_exam,
        schema=schemas.SimuExamPayload,
        module="app.tasks.simulation_tasks",
        bound=True,
    ),
    constants.TASK_SIMU_GRADUATE: TaskContract(
        name=constants.TASK_SIMU_GRADUATE,
        definition=definitions.simu_graduate,
        schema=schemas.SimuGraduatePayload,
        module="app.tasks.simulation_tasks",
        bound=True,
    ),
}

__all__ = ["TaskContract", "TASK_CATALOG"]
