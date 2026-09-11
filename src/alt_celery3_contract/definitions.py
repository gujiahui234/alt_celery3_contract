"""Declarative contract functions for the alt_celery3 Celery tasks.

Every function below mirrors the *public calling signature* of one task in
``alt_celery3`` — parameter names, type annotations and defaults are copied
from the source, while ``bind=True`` task instances have had their leading
``self`` argument stripped.

The function bodies intentionally raise :class:`NotImplementedError`: these
are **contracts, not implementations**. No business logic (database access,
LLM calls, third-party imports) is carried by this package. Producers use
these signatures for typing, IDE support and offline validation; the actual
execution happens on the alt_celery3 workers.
"""

from __future__ import annotations

from typing import Any

from . import constants

#: Default rows per bulk INSERT (mirrors ``DEFAULT_BATCH_SIZE`` of the source).
DEFAULT_BATCH_SIZE = 5_000
#: Default number of concurrent writer threads (mirrors the source default).
DEFAULT_THREADS = 8
#: Default number of universities requested per LLM run.
DEFAULT_UN_COUNT = 3


def add(x: int, y: int) -> int:
    """Contract of ``tasks.example.add``: return the sum of two integers.

    Args:
        x: First addend.
        y: Second addend.

    Returns:
        The integer sum of ``x`` and ``y``.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def scheduled_add(x: int, y: int) -> dict[str, Any]:
    """Contract of ``tasks.scheduled.add``: periodic addition with bookkeeping.

    The task records its own request id so the outcome of scheduled runs can
    be retrieved from the result backend later.

    Args:
        x: First addend.
        y: Second addend.

    Returns:
        Dictionary with the sum, request id, whether the last-run pointer was
        recorded and a UTC timestamp of the execution.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def try_mysql() -> dict[str, Any]:
    """Contract of ``tasks.db.try_mysql``: probe the ``web_db`` connectivity.

    Returns:
        Dictionary with ``ok``, connection metadata (without credentials),
        the measured ``latency_ms`` and a UTC ``checked_at`` timestamp. On
        failure ``ok`` is ``False`` and ``error`` carries the message.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def get_one_student() -> dict[str, Any]:
    """Contract of ``tasks.db.get_one_student``: persist one simulated student.

    Returns:
        Dictionary with ``ok``, the stored ``student`` fields and the number
        of ``affected_rows``. On failure ``ok`` is ``False`` and ``error``
        carries the message.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def generate_many_students(
    numbers: int,
    birthday_min: str | None = None,
    birthday_max: str | None = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    threads: int = DEFAULT_THREADS,
) -> dict[str, Any]:
    """Contract of ``tasks.db.generate_many_students``: million-scale inserts.

    The worker validates the request, splits ``numbers`` into ``batch_size``
    chunks distributed over a thread pool, and streams each batch through a
    dedicated MySQL connection using bulk INSERTs.

    Args:
        numbers: Total number of students to generate (must be positive).
        birthday_min: Lower bound of the birthday window — ``"2000"``,
            ``"2000-09"``, ``"2000-09-01"`` or ``None`` for unbounded.
        birthday_max: Upper bound of the birthday window (same formats).
        batch_size: Rows per bulk insert (clamped to ``[100, 50000]``).
        threads: Concurrent writer threads (clamped to ``[1, 32]``).

    Returns:
        Dictionary with ``ok``, ``requested``, ``inserted``, timing/rate
        statistics, the effective ``batch_size``/``threads``, the assigned
        ``id_start``/``id_end`` (AUTO_INCREMENT range) and a UTC
        ``finished_at`` timestamp. On failure ``ok`` is ``False`` and
        ``error`` carries the message.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def init_web_db() -> dict[str, Any]:
    """Contract of ``tasks.db.init_web_db``: rebuild the databases (destructive).

    Returns:
        Dictionary with ``ok``, the dropped/created databases and users, the
        created ``tables`` list, whether ``enrollment_status`` needed an
        in-place migration and a UTC ``finished_at`` timestamp. On failure
        ``ok`` is ``False`` and ``error`` carries the message.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def get_un_groups(count: int = DEFAULT_UN_COUNT) -> dict[str, Any]:
    """Contract of ``tasks.ai.get_un_groups``: LLM university collection.

    Asks the SiliconFlow chat model for ``count`` universities together with
    their major groups, de-duplicates the answer against the database and
    persists only the new rows.

    Args:
        count: Number of universities to request from the model (1..20).

    Returns:
        Dictionary with ``ok``, ``requested``, ``fetched``, dedup counters
        (``skipped_universities`` / ``skipped_major_groups``), insert
        counters, the stored ``universities`` payload and a UTC
        ``finished_at`` timestamp. On failure ``ok`` is ``False`` and
        ``error`` carries the message.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def simu_ncee(ncee_year: int, threads: int = DEFAULT_THREADS) -> dict[str, Any]:
    """Contract of ``tasks.simu.ncee``: simulate the college entrance exam.

    Args:
        ncee_year: Exam year; the exam date is ``{ncee_year}-06-20``.
        threads: Concurrent writer threads (clamped to ``[1, 32]``).

    Returns:
        Dictionary with ``ok``, ``examined`` (students scored),
        ``status_updated``, timing statistics and a UTC ``finished_at``
        timestamp. On failure ``ok`` is ``False`` and ``error`` carries the
        message.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def simu_admission(
    ncee_year: int, threads: int = DEFAULT_THREADS
) -> dict[str, Any]:
    """Contract of ``tasks.simu.admission``: tier-based university admission.

    Args:
        ncee_year: Exam year; students with scores in that year are admitted.
        threads: Concurrent writer threads (clamped to ``[1, 32]``).

    Returns:
        Dictionary with ``ok``, ``admitted``, per-nature admission counts and
        timing statistics. On failure ``ok`` is ``False`` and ``error``
        carries the message.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def simu_exam(academic_year: int, threads: int = DEFAULT_THREADS) -> dict[str, Any]:
    """Contract of ``tasks.simu.exam``: in-university exam simulation.

    Args:
        academic_year: Starting year of the academic year (e.g. 2027).
        threads: Concurrent writer threads (clamped to ``[1, 32]``).

    Returns:
        Dictionary with ``ok``, ``students_examined``, ``exams_recorded``
        and timing statistics. On failure ``ok`` is ``False``.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


def simu_graduate(
    graduate_year: int, threads: int = DEFAULT_THREADS
) -> dict[str, Any]:
    """Contract of ``tasks.simu.graduate``: graduation with GPA computation.

    Args:
        graduate_year: Graduation year; graduation date is July 1st.
        threads: Concurrent writer threads (clamped to ``[1, 32]``).

    Returns:
        Dictionary with ``ok``, ``graduated``, ``without_scores``,
        ``average_gpa`` and timing statistics. On failure ``ok`` is ``False``.

    Raises:
        NotImplementedError: Always — declarative contract only.
    """
    raise NotImplementedError


__all__ = [
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
    "constants",
]
