# Exercise Material

## Goal

Port the provided legacy COBOL banking module to modern Python while preserving the business logic and making the solution testable, readable, and safe.

## Context

The legacy module calculates debit interest on bank accounts and stores accounting movements. The original implementation uses procedural COBOL style, compact identifiers, and legacy error handling patterns.

## What the learner receives (self-contained package)

- `legacy_code.cob` - COBOL source to analyze and port
- `test_interest_calculator.py` - unit tests the solution should pass locally
- `exercise_material.md` - this problem statement
- `evaluation_guidelines.md` - transparent scoring rules used by the assessment agent

## Required Output

Submit a single Python file named `solution.py` implementing a class `InterestCalculator`.

## Functional Requirements (must be preserved)

Implement `InterestCalculator` with public methods that support:

1. Interest calculation
  - Formula: `interest = (principal * annual_rate * days) / 365`
  - The rate is already decimal (example: `0.035` = `3.5%`)
2. Input validation
  - Negative balance -> raise an error
  - Annual rate > `1.0` -> raise an error
  - `days == 0` -> zero interest and unchanged final balance
3. Movement persistence
  - Use in-memory SQLite (`:memory:`)
  - Save movement with progressive integer ID
  - Store amount and type (`"C"` / `"D"`)
4. Retrieval of saved movements
  - Return a testable list structure

## Required Technical Interface

The test suite expects a class with this public API:

- `InterestCalculator`
- `calculate_interest(balance, annual_rate, days)`
- `save_movement(amount, type_)`
- `get_movements()`

The exact implementation is flexible if the tests pass and the behavior matches the requirements.

## Transparent Scoring Metrics (visible to the learner)

Your submission is scored out of 100 using measurable criteria. The AI assessment agent uses tool outputs (tests, static checks, security checks) to assign these scores.


| Criterion                    | Max Points | Measurable Evidence                              | What is considered sufficient                                                        |
| ---------------------------- | ---------- | ------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Correctness                  | 40         | Functional test pass rate                        | Most functional tests pass; full points when all functional tests pass               |
| Error Handling               | 10         | Error-related tests + raised exceptions/messages | Invalid inputs produce appropriate exceptions and messages                           |
| Type Hints                   | 15         | Static code analysis + quality tests             | Public methods have parameter and return annotations                                 |
| Docstrings                   | 10         | Static code analysis + quality tests             | Class and public methods include meaningful docstrings                               |
| In-memory SQLite Persistence | 15         | Persistence tests                                | Movements are stored/retrieved correctly with isolated `:memory:` DB per instance    |
| Architecture                 | 10         | Class structure analysis                         | `InterestCalculator` exists with clear public methods and separated responsibilities |


## Mandatory Conditions (insufficient if violated)

The submission is considered insufficient if any of the following happens:

- The module cannot be imported/executed
- `InterestCalculator` is missing
- Most functional tests fail (less than 60% overall pass rate)
- Dangerous imports/patterns are detected by security analysis

## Notes for the Learner

- The evaluation is performed by an AI agent, but it is expected to rely on deterministic tool evidence (tests and analyzers) for fairness.
- Passing all tests is necessary but not always sufficient for full score (documentation and code quality also matter).
- The scoring categories and weights above are the same categories returned by the evaluator output.

## Submission Format

Create a zip file containing exactly these files:

```
solution.py
pytest_output.txt
```

- **`solution.py`** — your Python implementation containing the `InterestCalculator` class
- **`pytest_output.txt`** — the full terminal output from running the provided tests locally:
  ```bash
  pytest test_interest_calculator.py -v > pytest_output.txt 2>&1
  ```

Do not submit tests, extra files, or the original exercise materials.

