"""Pydantic payload schemas for the alt_celery3 task contracts.

One model is generated for every task whose input surface has more than one
business argument or whose execution is complex enough to deserve declared
validation constraints. All constraints are *declarative only* — they are
derived from the documented behaviour of the source tasks (clamping ranges,
date-window formats) and contain no business logic.

Tasks with zero arguments (``try_mysql``, ``get_one_student``,
``init_web_db``) have no payload model on purpose.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

#: Birthday-window format accepted by ``generate_many_students``:
#: ``YYYY``, ``YYYY-MM`` or ``YYYY-MM-DD``.
_BIRTHDAY_PATTERN = r"^\d{4}(?:-\d{2})?(?:-\d{2})?$"


class _ContractModel(BaseModel):
    """Shared base for every payload schema.

    Extra keys are rejected so a producer cannot silently send misspelled
    arguments that the worker would ignore (JSON serializer semantics).
    """

    model_config = ConfigDict(extra="forbid")


class AddPayload(_ContractModel):
    """Payload of ``tasks.example.add``.

    Attributes:
        x: First addend.
        y: Second addend.
    """

    x: int
    y: int


class ScheduledAddPayload(_ContractModel):
    """Payload of ``tasks.scheduled.add`` (periodic addition example).

    Attributes:
        x: First addend.
        y: Second addend.
    """

    x: int
    y: int


class GenerateManyStudentsPayload(_ContractModel):
    """Payload of ``tasks.db.generate_many_students``.

    The worker clamps ``batch_size`` to ``[100, 50000]`` and ``threads`` to
    ``[1, 32]``; the schema declares these bounds so invalid requests fail
    at the producer instead of inside the worker.

    Attributes:
        numbers: Total number of students to generate (must be positive).
        birthday_min: Lower bound of the birthday window (``YYYY``,
            ``YYYY-MM`` or ``YYYY-MM-DD``), or ``None`` for unbounded.
        birthday_max: Upper bound of the birthday window (same formats).
        batch_size: Rows per bulk INSERT.
        threads: Concurrent writer threads.
    """

    numbers: int = Field(ge=1, description="Total number of students to generate.")
    birthday_min: str | None = Field(
        default=None,
        pattern=_BIRTHDAY_PATTERN,
        description="Birthday lower bound: YYYY, YYYY-MM or YYYY-MM-DD.",
    )
    birthday_max: str | None = Field(
        default=None,
        pattern=_BIRTHDAY_PATTERN,
        description="Birthday upper bound: YYYY, YYYY-MM or YYYY-MM-DD.",
    )
    batch_size: int = Field(
        default=5_000,
        ge=100,
        le=50_000,
        description="Rows per bulk INSERT (worker clamps to [100, 50000]).",
    )
    threads: int = Field(
        default=8,
        ge=1,
        le=32,
        description="Concurrent writer threads (worker clamps to [1, 32]).",
    )


class GetUnGroupsPayload(_ContractModel):
    """Payload of ``tasks.ai.get_un_groups``.

    The worker clamps ``count`` to ``[1, 20]``; the schema surfaces that
    constraint so producers validate before dispatch.

    Attributes:
        count: Number of universities to request from the LLM.
    """

    count: int = Field(
        default=3,
        ge=1,
        le=20,
        description="Number of universities to request (worker clamps to [1, 20]).",
    )


class SimuNceePayload(_ContractModel):
    """Payload of ``tasks.simu.ncee`` (高考模拟).

    Attributes:
        ncee_year: Exam year; the exam date is fixed at ``{ncee_year}-06-20``.
        threads: Concurrent writer threads.
    """

    ncee_year: int = Field(description="Exam year (exam date: June 20th).")
    threads: int = Field(
        default=8,
        ge=1,
        le=32,
        description="Concurrent writer threads (worker clamps to [1, 32]).",
    )


class SimuAdmissionPayload(_ContractModel):
    """Payload of ``tasks.simu.admission`` (高校录取模拟).

    Attributes:
        ncee_year: Exam year whose cohort gets admitted.
        threads: Concurrent writer threads.
    """

    ncee_year: int = Field(description="Exam year of the cohort to admit.")
    threads: int = Field(
        default=8,
        ge=1,
        le=32,
        description="Concurrent writer threads (worker clamps to [1, 32]).",
    )


class SimuExamPayload(_ContractModel):
    """Payload of ``tasks.simu.exam`` (本科考试模拟).

    Attributes:
        academic_year: Starting year of the academic year.
        threads: Concurrent writer threads.
    """

    academic_year: int = Field(description="Starting year of the academic year.")
    threads: int = Field(
        default=8,
        ge=1,
        le=32,
        description="Concurrent writer threads (worker clamps to [1, 32]).",
    )


class SimuGraduatePayload(_ContractModel):
    """Payload of ``tasks.simu.graduate`` (毕业模拟).

    Attributes:
        graduate_year: Graduation year (graduation date: July 1st).
        threads: Concurrent writer threads.
    """

    graduate_year: int = Field(description="Graduation year (date: July 1st).")
    threads: int = Field(
        default=8,
        ge=1,
        le=32,
        description="Concurrent writer threads (worker clamps to [1, 32]).",
    )


__all__ = [
    "AddPayload",
    "ScheduledAddPayload",
    "GenerateManyStudentsPayload",
    "GetUnGroupsPayload",
    "SimuNceePayload",
    "SimuAdmissionPayload",
    "SimuExamPayload",
    "SimuGraduatePayload",
]
