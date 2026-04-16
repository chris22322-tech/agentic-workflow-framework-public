# Evaluation Report Template

Output artifact for [Stage 6: Evaluate](../stages/06-evaluate.md).

Validate that the agent works correctly, handles edge cases, and produces output comparable to the manual process.

---

## 1. Test Cases

Design a minimum of 5 test cases representing different profiles.

| Test Case | Profile | Purpose | Result | Notes |
|---|---|---|---|---|
| *e.g., Happy path* | *e.g., All data available, no anomalies* | *e.g., Verify basic end-to-end flow* | *Pass / Fail / Partial* | |
| *e.g., At-risk subject* | *e.g., Declining metrics, open issues* | *e.g., Verify risk identification* | | |
| *e.g., Data gap* | *e.g., One or more sources return empty/error* | *e.g., Verify graceful degradation* | | |
| *e.g., Sparse data* | *e.g., Limited history, new subject* | *e.g., Verify no over-interpretation* | | |
| *e.g., Complex case* | *e.g., Mixed signals, multiple dimensions* | *e.g., Verify nuance handling* | | |

---

## 2. Quality Assessment

| Dimension | What to Assess | Assessment |
|---|---|---|
| **Correctness** | Does the agent retrieve the right data and produce accurate analysis? | |
| **Completeness** | Does the agent cover all aspects the manual process covers? | |
| **Quality** | Is the written output at professional standard? | |
| **Robustness** | How does the agent handle missing data, API failures, or unusual inputs? | |
| **Efficiency** | Is the agent actually saving time? (agent run time + human review vs. manual) | |
| **HIL Effectiveness** | Are the interrupt points at the right places? Is the surfaced information useful? | |
| **Trajectory** | Did the agent take the right path through the flow — correct action sequence, no unnecessary loops, no skipped steps? | |

---

## 3. Failure Modes

| Failure Mode | Observed Behaviour | Root Cause | Category | Severity |
|---|---|---|---|---|
| *e.g., Missed risk signal* | *What happened* | *Why it happened* | *Tool / Prompt / Graph / Scope* | *Critical / High / Medium / Low* |
| | | | | |
| | | | | |
| | | | | |

---

## 4. Iteration Log

Track each change you make and its effect on test cases.

| Date | Change Made | Test Cases Affected | Result |
|---|---|---|---|
| *Date* | *What you changed* | *Which test cases you re-ran* | *Pass / Fail / Partial* |
| | | | |
| | | | |
| | | | |
| | | | |

---

## 5. Graduation Criteria

The agent is ready for production use when all criteria are met.

- [ ] All 5+ test cases pass without major human corrections
- [ ] Total time (agent + human review) is less than 50% of the manual process time
- [ ] No critical failures in the last 3 evaluation rounds
- [ ] At least one colleague has reviewed and validated the output quality
- [ ] Error handling has been tested for all identified failure modes
