#!/usr/bin/env python3
"""Verify that the contract package is signature-compatible with alt_celery3.

The script performs two layers of checks:

1. **Internal consistency** (always runs, needs only this package):
   every ``TaskName`` has a catalog entry, every contract function raises
   ``NotImplementedError``, and each payload schema mirrors the parameters
   (names, order, defaults) of its contract function.

2. **Source compatibility** (only when the ``alt_celery3`` application can be
   imported from the current working directory / ``PYTHONPATH``): every
   contract signature is compared, via :mod:`inspect`, against the runtime
   signature of the registered Celery task (``task.run`` — bound ``self``
   already excluded by method binding).

Run it from the ``alt_celery3`` project root::

    PYTHONPATH=/path/to/alt_celery3_contract/src python scripts/verify_contracts.py

Exit code is ``0`` when all checks pass, ``1`` otherwise.
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from typing import Any, get_type_hints

from alt_celery3_contract import TASK_CATALOG, TaskContract, TaskName

_ERRORS: list[str] = []
_CHECKED = 0


def _fail(message: str) -> None:
    """Record a verification failure.

    Args:
        message: Human-readable description of the mismatch.
    """
    _ERRORS.append(message)


def _norm(annotation: Any) -> str:
    """Normalise an annotation for comparison.

    Args:
        annotation: A raw annotation object or string.

    Returns:
        A canonical string representation (``None`` for empty annotations).
    """
    if annotation is inspect.Parameter.empty:
        return "None"
    return str(annotation).replace("typing.", "").replace(" ", "")


def check_internal(contract: TaskContract) -> None:
    """Verify the internal consistency of one contract record.

    Args:
        contract: The catalog entry under inspection.
    """
    global _CHECKED
    _CHECKED += 1
    prefix = f"[catalog] {contract.name}"

    # The contract function must be a pure declaration: call it with placeholder
    # values for its required parameters and expect NotImplementedError.
    required = [
        param
        for param in inspect.signature(contract.definition).parameters.values()
        if param.default is inspect.Parameter.empty
        and param.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
    ]
    try:
        contract.definition(*[None] * len(required))
    except NotImplementedError:
        pass
    except Exception as exc:  # pragma: no cover - defensive
        _fail(f"{prefix}: definition body raised {type(exc).__name__}: {exc}")
        return

    definition_sig = inspect.signature(contract.definition)
    definition_hints = get_type_hints(contract.definition)

    # A payload schema must mirror the definition's parameters exactly.
    if contract.schema is None:
        if definition_sig.parameters:
            _fail(
                f"{prefix}: no schema declared but the contract takes "
                f"{list(definition_sig.parameters)!r}"
            )
        return

    schema_fields = contract.schema.model_fields
    schema_names = list(schema_fields)
    param_names = list(definition_sig.parameters)
    if schema_names != param_names:
        _fail(
            f"{prefix}: schema field order {schema_names} != parameter order "
            f"{param_names}"
        )
        return

    for name, field in schema_fields.items():
        param = definition_sig.parameters[name]
        if not field.is_required() and param.default != field.default:
            _fail(
                f"{prefix}.{name}: schema default {field.default!r} != "
                f"definition default {param.default!r}"
            )
        field_hint = schema_fields[name].annotation
        if field_hint is not None and _norm(
            str(field_hint)
        ) != _norm(definition_hints.get(name)):
            # Only compare when both sides declare something concrete.
            declared = _norm(definition_hints.get(name))
            schema_hint = _norm(str(field_hint))
            if declared != "None" and declared != schema_hint:
                _fail(
                    f"{prefix}.{name}: schema annotation {schema_hint} != "
                    f"definition annotation {declared}"
                )


def check_against_source(contract: TaskContract, task: Any) -> None:
    """Compare one contract against the runtime Celery task registration.

    Args:
        contract: The catalog entry under inspection.
        task: The Celery task instance from ``celery_app.tasks``.
    """
    global _CHECKED
    _CHECKED += 1
    prefix = f"[source] {contract.name}"

    run = task.run
    source_sig = inspect.signature(run)
    contract_sig = inspect.signature(contract.definition)

    source_params = list(source_sig.parameters)
    contract_params = list(contract_sig.parameters)
    if source_params != contract_params:
        _fail(
            f"{prefix}: parameter mismatch source={source_params} "
            f"contract={contract_params}"
        )
        return

    for name in source_params:
        src = source_sig.parameters[name]
        dst = contract_sig.parameters[name]
        if src.default != dst.default:
            _fail(
                f"{prefix}.{name}: default mismatch source={src.default!r} "
                f"contract={dst.default!r}"
            )
        src_ann = _norm(src.annotation)
        dst_ann = _norm(dst.annotation)
        if src_ann != dst_ann and src_ann != "Any" and dst_ann != "None":
            _fail(
                f"{prefix}.{name}: annotation mismatch source={src_ann} "
                f"contract={dst_ann}"
            )

    src_ret = _norm(source_sig.return_annotation)
    dst_ret = _norm(contract_sig.return_annotation)
    if src_ret != dst_ret and src_ret != "None":
        _fail(
            f"{prefix}: return annotation mismatch source={src_ret} "
            f"contract={dst_ret}"
        )


def main() -> int:
    """Run every verification layer and print a summary.

    Returns:
        Process exit code (0 = pass, 1 = failures found).
    """
    print(f"Verifying {len(TASK_CATALOG)} task contracts ...")

    # --- layer 1: internal consistency --------------------------------------
    for name, contract in TASK_CATALOG.items():
        if name != contract.name:
            _fail(f"[catalog] key {name!r} != contract.name {contract.name!r}")
        check_internal(contract)

    missing = {member.value for member in TaskName} - set(TASK_CATALOG)
    if missing:
        _fail(f"[catalog] TaskName members without catalog entry: {sorted(missing)}")

    # --- layer 2: source compatibility (best effort) -------------------------
    try:
        # ``app`` lives in the caller's working directory (the alt_celery3
        # root); make it importable regardless of how the script is invoked.
        sys.path.insert(0, str(Path.cwd()))
        from app.celery_app import celery_app  # noqa: PLC0415 — optional import.

        # Import the modules listed in ``include`` so the task registry is
        # fully populated (Celery does this lazily otherwise).
        celery_app.loader.import_default_modules()
    except ImportError as exc:
        print(
            f"[skip] alt_celery3 application not importable ({exc}); "
            "source-compatibility layer not executed."
        )
    else:
        for name, contract in TASK_CATALOG.items():
            task = celery_app.tasks.get(name)
            if task is None:
                _fail(f"[source] {name}: not registered on the Celery app")
                continue
            check_against_source(contract, task)

    print(f"Checks executed: {_CHECKED}")
    if _ERRORS:
        print(f"\nFAILED with {len(_ERRORS)} problem(s):")
        for error in _ERRORS:
            print(f"  - {error}")
        return 1
    print("All contract checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
