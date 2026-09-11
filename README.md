# alt_celery3_contract

Declarative, strongly-typed **task contracts** for the
[`alt_celery3`](https://github.com/ashida2016/alt_celery3) Celery
application.

This package is a pure *contract layer* extracted (statically) from
`alt_celery3`. It declares **what** the tasks accept and **what** they
return — never **how** they do it. There is no database access, no LLM call
and no third-party business dependency inside; the only runtime requirement
is `pydantic`.

| Module | Content |
|---|---|
| `constants` | `TaskName` enum + `TASK_*` aliases for all 11 canonical task names |
| `schemas` | Pydantic v2 payload models with declared field constraints |
| `definitions` | Contract functions: signature mirrors only (`raise NotImplementedError`) |
| `catalog` | `TASK_CATALOG` — task name → contract function / schema / source module |

## Covered tasks (11)

| Task name | Contract function | Payload schema |
|---|---|---|
| `tasks.example.add` | `add(x, y)` | `AddPayload` |
| `tasks.scheduled.add` | `scheduled_add(x, y)` | `ScheduledAddPayload` |
| `tasks.db.try_mysql` | `try_mysql()` | — |
| `tasks.db.get_one_student` | `get_one_student()` | — |
| `tasks.db.generate_many_students` | `generate_many_students(numbers, ...)` | `GenerateManyStudentsPayload` |
| `tasks.db.init_web_db` | `init_web_db()` | — |
| `tasks.ai.get_un_groups` | `get_un_groups(count=3)` | `GetUnGroupsPayload` |
| `tasks.simu.ncee` | `simu_ncee(ncee_year, threads=8)` | `SimuNceePayload` |
| `tasks.simu.admission` | `simu_admission(ncee_year, threads=8)` | `SimuAdmissionPayload` |
| `tasks.simu.exam` | `simu_exam(academic_year, threads=8)` | `SimuExamPayload` |
| `tasks.simu.graduate` | `simu_graduate(graduate_year, threads=8)` | `SimuGraduatePayload` |

`bind=True` tasks had their leading `self` argument stripped; the contract
signature equals the producer-facing signature.

## Installation

```bash
# From GitHub (recommended for producers of alt_celery3)
pip install git+https://github.com/ashida2016/alt_celery3_contract.git

# Development install
git clone https://github.com/ashida2016/alt_celery3_contract
cd alt_celery3_contract
pip install -e .[dev,docs]
```

Or with conda: `conda env create -f environment.yml && conda activate alt-celery3-contract`.

## Usage

### 1. Reference task names without magic strings

```python
from alt_celery3_contract import TaskName, TASK_GET_UN_GROUPS

result = celery_app.send_task(TaskName.TASK_GET_UN_GROUPS, kwargs={"count": 5})
assert TASK_GET_UN_GROUPS == "tasks.ai.get_un_groups"
```

### 2. Validate payloads before dispatch

```python
from alt_celery3_contract import TASK_CATALOG, TaskName

contract = TASK_CATALOG[TaskName.TASK_GENERATE_MANY_STUDENTS]
kwargs = contract.validate_kwargs(
    {"numbers": 100_000, "birthday_min": "2000-01-01", "threads": 16}
)
celery_app.send_task(contract.name, kwargs=kwargs)
# pydantic.ValidationError is raised here — before the broker round trip —
# when a constraint is violated (e.g. threads=99, bad birthday format).
```

### 3. Type-hint producer code against contract stubs

```python
from alt_celery3_contract.definitions import generate_many_students

def enqueue_students(numbers: int) -> None:
    # IDE autocompletion / mypy use the exact signature served by the workers.
    _sig: type = type(generate_many_students)
    celery_app.send_task("tasks.db.generate_many_students", kwargs={
        "numbers": numbers,
        "batch_size": 5_000,
        "threads": 8,
    })
```

> Contract functions raise `NotImplementedError` by design — call them only
> for signature introspection (`inspect.signature`), never for execution.

### 4. Verify contract/source compatibility

From the `alt_celery3` project root (both packages importable):

```bash
PYTHONPATH=../alt_celery3_contract/src python \
    ../alt_celery3_contract/scripts/verify_contracts.py
```

The script checks catalog consistency (always) and, when `app.celery_app`
is importable, compares every contract signature with the registered Celery
task signature via `inspect`.

## Documentation

Sphinx sources live in `docs/` and are hosted on Read the Docs
(see `.readthedocs.yaml`). Build locally:

```bash
pip install -e .[docs]
sphinx-build -b html docs docs/_build/html
```

## Regenerating / evolving the contract

The contract mirrors `alt_celery3`. When a task in `alt_celery3` changes
its name, parameters or defaults, update the contract in the same pull
request and run `scripts/verify_contracts.py` — the CI gate is exactly this
compatibility check.

## License

MIT
