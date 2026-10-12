# Delivery

Use at the requested endpoint. Completion means evidence for the agreed outcome;
it does not require every project to deploy or become a production service.

## Compare the result to the contract

For substantial work, record an acceptance matrix in an existing work record or
delivery note. A small task can report the same information in a few sentences.

| Criterion | Evidence | State | Remaining action |
| --- | --- | --- | --- |
| A draft survives reopening | Named integration test and observed run | Passed | None |
| Hosted login works | Local simulation only; hosted credentials unavailable | Not verified | Run the documented hosted check |

Use exact commands or artifact links where useful. Identify what was exercised
and under which environment. Report failures and not-run checks explicitly.
Make claims as narrow as the method behind them: "dependency audit found no
known advisories" rather than "secure", and observed counts rather than
compliance percentages. Separate acceptance failures from optional future
improvements.

Review both the intended behavior and the quality of the changes. Inspect the
actual delivery for placeholders in functional paths, swallowed errors, missing
failure handling, exposed secrets, and inaccurate setup instructions where
applicable. Fix issues inside the agreed scope and validate the fixes.

## Make the result usable

Provide setup, required configuration names, a runnable example, and the relevant
verification command. Use example values instead of secrets. Ensure a new human
or agent can locate intent, current implementation, evidence, and next steps.
When reproducibility matters, record input provenance and dependency versions.

Prepare a concrete artifact before seeking any missing publication or deployment
authorization. Existing explicit authorization remains valid without a second
approval. Ask about destination, visibility, or cost only when the request and
environment leave it open.

After an authorized publish or deploy, verify the actual destination and report
its link and status; a started build or push command is not a publication.
External issues, messages, and scheduled monitors are separate actions that
need their own request.

If an external prerequisite blocks completion, leave the working result, exact
blocker, and next command or action, and report the blocked requirement as
not delivered. A plan-only request is complete when its plan is ready; an
implementation request still needs its authorized implementation.
