# Framework Application Checklist

Use this checklist when applying the framework to a new workflow. Each item maps to a specific stage output or artifact.

---

## Stage 1: Decompose (all roles)

- [ ] Listed all responsibility areas for the role
- [ ] Identified 8+ discrete workflows
- [ ] Each workflow has: trigger, frequency, time cost, systems, output, automation potential
- [ ] Automation potential scoring uses the High/Medium/Low criteria defined in Stage 1
- [ ] Workflow dependencies documented (shared data sources, sequential dependencies, independent workflows)
- [ ] Initiated compliance and legal conversations for AI/LLM data processing (see Scope Document Section 6 for pre-flight checklist)

## Stage 2: Select (all roles)

- [ ] Scored all High/Medium candidates on the 6 selection criteria
- [ ] Calculated weighted composite scores
- [ ] Assessed Organisational Readiness for the top candidate (team consulted, adoption signals documented)
- [ ] Checked "when NOT to automate" list
- [ ] Written a selection justification with known risks

## Stage 3: Scope (all roles, with engineer input on Integration Requirements)

- [ ] Mapped every step of the workflow as-is (minimum 8 steps -- if fewer, break steps down further)
- [ ] Each step has: action, input, output, decision logic, boundary tag (see [Should I Automate?](decision-trees.md#should-i-automate-this-step))
- [ ] Completed data inventory with access methods
- [ ] Integration requirements listed
- [ ] Constraints and assumptions documented
- [ ] Per-step time estimates included in workflow map
- [ ] At least one HIL checkpoint exists in the first version
- [ ] Compliance readiness pre-flight completed — all six conversations initiated and status recorded in Scope Document Section 6

## Stage 4: Design (engineer, with workflow owner collaboration)

- [ ] Scope-to-action mapping table created (every scope step accounted for, consolidation rationale documented)
- [ ] Agent flow drawn (visual or text diagram)
- [ ] Memory fields defined with explicit types and read/write traceability
- [ ] Each action has: purpose, tools, logic summary, prompt pattern (if applicable)
- [ ] HIL checkpoints specify what is surfaced and what input is expected
- [ ] Error handling defined for each failure mode
- [ ] Selected appropriate design pattern(s) (see [Design Pattern Decision Tree](decision-trees.md#what-design-pattern-should-i-use))

## Stage 5: Build (engineer)

- [ ] Project structure follows the convention for your chosen platform
- [ ] All tools implemented as thin wrappers with error handling
- [ ] All actions implemented
- [ ] Prompts externalised from action code
- [ ] Config externalised (scoring rubric, thresholds, model settings)
- [ ] Agent runs end-to-end with test data
- [ ] Durable persistence configured before deployment (not just in-memory)
- [ ] HIL flow works (pause and resume)

## Stage 6: Evaluate (all roles)

- [ ] 5+ test cases designed covering different profiles
- [ ] Edge cases included (missing data, unusual inputs, boundary conditions)
- [ ] Expected output or evaluation criteria documented for each test case
- [ ] All test cases executed
- [ ] Quality compared against manual output
- [ ] Failure modes documented
- [ ] Iteration backlog created and prioritised
- [ ] Graduation criteria assessed
