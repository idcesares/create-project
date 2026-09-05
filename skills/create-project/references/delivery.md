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
Avoid broad "security passed" or numerical compliance claims unsupported by a
defined method. Separate acceptance failures from optional future improvements.

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
authorization. Existing explicit authorization remains valid; do not require a
ceremonial second approval. Resolve a missing destination, visibility, or cost
decision only if it cannot be inferred from the request and environment.

After an authorized publish or deploy, verify the actual destination and report
its link and status. Do not mark a publication complete because a local build or
push command merely started. Do not create external issues, send messages, or
schedule monitors as an incidental part of delivery.

If an external prerequisite blocks completion, leave the working result, exact
blocker, and next command or action. Do not describe the blocked requirement as
delivered. A plan-only request is complete when its requested plan is ready;
an implementation request still needs its authorized implementation.
