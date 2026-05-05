# Evaluation Guidelines

Use the automated tests as the primary source of truth for behavior. Use static analysis and security analysis to score non-functional criteria. The assessment must remain transparent, evidence-based, and reproducible.

## Evaluation Mode

- The final evaluation is produced by an AI assessment agent.
- The AI agent must base scores on evidence from the submitted files (solution.py and pytest_output.txt), not intuition.

## Required Output Schema

Respond with ONLY this JSON shape (the exact schema is also restated at the end of the user prompt — follow that literally):

```json
{
  "breakdown": {
    "correctness": <int 0-40>,
    "error_handling": <int 0-10>,
    "type_hints": <int 0-15>,
    "docstring": <int 0-10>,
    "sqlite": <int 0-15>,
    "architecture": <int 0-10>
  },
  "message": "<string: candidate-facing feedback, ≤120 words>"
}
```

The total score is computed by the platform as `sum(breakdown.values())`. Do NOT add `total_score`, `passed`, or `feedback` fields.

## Transparent Measurable Criteria (weights)

Map the evaluation to the following measurable criteria:

1. Correctness (40)
   - Evidence: automated test pass rate, especially core calculation and integration tests
   - Full score only when all relevant tests pass
2. Error handling (10)
   - Evidence: error-focused tests (`ValueError` on invalid inputs), message relevance
3. Type hints (15)
   - Evidence: static analysis of annotations on public methods + unit tests checking signatures
4. Docstrings (10)
   - Evidence: static analysis + unit tests checking class/public-method docstrings
5. In-memory SQLite persistence (15)
   - Evidence: persistence tests (save/retrieve, IDs, instance isolation)
6. Architecture (10)
   - Evidence: class existence, expected public methods, separation of responsibilities, readability

## Scoring Bands

Use these bands to calibrate the tone of your `message`. The tone MUST match the band — do not write "Excellent" for a Strong submission or "Strong" for an Acceptable one.

| Band | Score | What it means |
|------|-------|---------------|
| Excellent | 90–100 | All or nearly all tests pass; type hints complete; docstrings present and meaningful; SQLite isolation fully correct; clean architecture |
| Strong | 75–89 | Most tests pass (≥80%); minor gaps in type hints, docstrings, or persistence isolation |
| Acceptable | 60–74 | Core calculation works; at least one significant gap (e.g. error handling missing, SQLite not isolated, docstrings absent) |
| Below bar | 0–59 | More than 40% of tests fail, or required class missing, or dangerous code detected |

## Mandatory Conditions

The submission is insufficient (`passed = false`) if any of these conditions occur:

- Security analysis returns `DANGEROUS`
- The solution cannot be imported or executed by the test runner
- Required class `InterestCalculator` is missing
- Less than 60% of the tests pass

## Scoring Principles (fairness / determinism)

- Prefer tool-derived metrics when available.
- If evidence is missing for a criterion, state the limitation in feedback.
- Do not reward unsupported claims.
- Keep scoring consistent with the measurable criteria listed in the problem statement.
- Use the reference solution as a behavioral benchmark when helpful, but never as the only source of truth.

## Message Rules

The `message` field (2-4 sentences, ≤120 words) must:

- state the outcome (passed / did not pass the bar)
- cite 1-2 concrete observations from what the candidate submitted
- explain which criteria cost them points
- give actionable next steps to improve the score
- contain no markdown headers, bullet lists, or code fences
