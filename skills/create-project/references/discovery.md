# Discovery and uncertainty

Read this when an unresolved question could change the outcome or invalidate
the implementation. Stop discovery when enough is known for the next useful
slice; the aim is to reduce decision risk, not survey every possible tool.

## Separate facts from decisions

Inspect existing artifacts for requirements, conventions, prior decisions, and
available capabilities. Mark unsupported statements as assumptions. Clarify
ambiguous domain terms when they change data or behavior: for example, whether
an "account" means a person, an organization, or a billing relationship.

Research technical facts using primary documentation, source code, or papers
when versions, APIs, compatibility, or feasibility matter. Record the source,
date checked, relevant version, finding, and the decision it informs. Prefer a
small relevant comparison to a broad landscape report. If sources cannot be
accessed, state that limit and avoid claiming a current fact was verified.

User decisions concern outcomes and tradeoffs: who this serves, what can be
excluded, where private data may go, and acceptable ongoing cost. Ask the
smallest question that unlocks progress, including a recommended default when
evidence supports one. Do not repeat answered questions.

## Map uncertainty only when it has dependencies

For a large fuzzy effort, keep a compact table in the existing context record:

| Question | Why it matters | Depends on | Cheapest useful evidence | State |
| --- | --- | --- | --- | --- |
| Can ingestion preserve source identifiers? | Reproducible citations | Input format | Parse representative samples | Open |
| Which storage model supports the query? | Retrieval behavior | Query examples | Run queries on a small fixture | Waiting for examples |

Resolve questions that unlock others first. Each resolution records evidence,
decision, remaining uncertainty, and affected acceptance criteria. Define a stop
condition for research, such as a supported API contract or a representative
benchmark. Reassess after a bounded attempt yields no new evidence; do not keep
researching or retrying services without a reason to expect a different result.

## Choose between research and prototype

- Use research for facts that already exist: an API limit, platform capability,
  published method, license term, or supported version.
- Use a prototype for behavior that must be observed: interaction quality,
  latency on representative inputs, state transitions, or model usefulness.
- Ask the user when neither technical evidence nor a prototype can choose the
  desired product tradeoff.

Before prototyping, write the hypothesis, smallest experiment, success measure,
time or resource bound, and the decision the result will unlock. Keep prototype
artifacts identifiable and record whether they are retained, adapted, or
discarded. Do not silently promote an experimental shortcut to production.

For architecture choices, compare only plausible options against actual
requirements, including operational burden and reversibility. Record the choice
and why the alternatives did not fit. Research-only requests end with findings
and a next step; they do not automatically become implementation projects.
