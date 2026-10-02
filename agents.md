```md
# FloodLens AI — Agent Workflow

## 1. Purpose

This document defines how the coding agent should work on FloodLens AI.

FloodLens uses **one primary coding agent with multiple operating modes** rather than multiple autonomous agents.

The objective is:

- Minimize token usage
- Avoid duplicated reasoning
- Preserve architecture
- Make small, verifiable changes
- Keep project state accurate
- Prevent unnecessary complexity

---

# 2. Agent Model

Use a single coding agent with four modes:

```text
              ┌─────────────┐
              │     PLAN    │
              │ Analyze     │
              │ & Design    │
              └──────┬──────┘
                     ↓
              ┌─────────────┐
              │    BUILD    │
              │ Implement   │
              └──────┬──────┘
                     ↓
              ┌─────────────┐
              │    CHECK    │
              │ Validate    │
              └──────┬──────┘
                     ↓
              ┌─────────────┐
              │    STATE    │
              │ Record      │
              └─────────────┘
```

Do not create separate autonomous Planner, Coder, Tester, or Documentation agents unless there is a concrete technical requirement.

---

# 3. Context Hierarchy

Use context in this order:

```text
1. system_prompt.md
        ↓
2. project_state.md
        ↓
3. architecture/agents.md
        ↓
4. Relevant source files
        ↓
5. Relevant tests
```

`project_state.md` is the source of truth for current project status.

Do not assume that something described in the architecture has already been implemented.

---

# 4. PLAN Mode

Use PLAN mode for:

- New features
- New modules
- Architecture changes
- ML pipeline changes
- Database changes
- Cross-layer functionality
- Features involving multiple files

### Process

1. Read `project_state.md`.
2. Identify the relevant module.
3. Retrieve only necessary files.
4. Identify dependencies.
5. Define the smallest viable implementation.
6. Identify tests.
7. Identify risks.

### Output

Keep the plan concise:

```text
Objective:
Relevant files:
Files to create:
Files to modify:
Implementation:
Tests:
Risks:
Definition of done:
```

Do not scan the entire repository.

Do not implement unrelated work during PLAN mode.

---

# 5. BUILD Mode

BUILD mode implements the approved task.

### Before coding

```text
Read state
   ↓
Retrieve relevant files
   ↓
Understand existing implementation
   ↓
Identify minimum changes
   ↓
Implement
```

### Rules

- Modify the minimum number of files necessary.
- Reuse existing utilities.
- Preserve existing interfaces where possible.
- Do not duplicate functionality.
- Do not perform unrelated refactoring.
- Maintain type safety.
- Add error handling.
- Add tests where appropriate.
- Follow the existing project architecture.

Prefer:

```text
Small change → Test → Continue
```

over:

```text
Large change → Test everything at the end
```

---

# 6. CHECK Mode

CHECK mode validates the implementation.

Validation should be proportional to the change.

### For backend changes

Check:

- API contracts
- Pydantic schemas
- Input validation
- Error handling
- HTTP behavior
- Model inference

### For frontend changes

Check:

- TypeScript
- Component behavior
- API integration
- Loading states
- Error states
- Rendering behavior

### For ML changes

Check:

- Data leakage
- Train/test separation
- Preprocessing
- Metrics
- Model inference
- Reproducibility

### For geospatial changes

Check:

- CRS
- Geometry validity
- Spatial joins
- Coordinates
- Distance/area calculations

### For full-stack changes

Test the affected vertical path rather than automatically testing the entire application.

---

# 7. STATE Mode

Use STATE mode after meaningful completed work.

Update:

```text
/ai_context/project_state.md
```

Record only verified facts:

```text
Completed:
Current:
Remaining:
Decisions:
Known issues:
```

Never mark something as implemented merely because code was generated.

Only record:

```text
IMPLEMENTED
```

after implementation and relevant validation.

Avoid turning `project_state.md` into a detailed development diary.

---

# 8. Context Retrieval Strategy

If Graphify or another context-retrieval system is available:

```text
User request
     ↓
project_state.md
     ↓
Identify relevant module
     ↓
Graphify/context retrieval
     ↓
Retrieve minimum sufficient files
     ↓
Implement
```

### Never

- Scan the entire repository for every request.
- Read unrelated modules.
- Re-read unchanged files unnecessarily.
- Reproduce entire source files in responses.
- Retrieve the entire frontend for a backend bug.
- Retrieve the entire ML pipeline for a UI change.

### Principle

> Minimum sufficient context, not minimum possible context.

Correctness always takes priority over token savings.

---

# 9. Task Routing

Use the following decision process:

```text
Is the task small and localized?
        │
       YES
        ↓
      BUILD
        │
        └── CHECK if necessary


Is the task complex or cross-layer?
        │
       YES
        ↓
      PLAN
        ↓
      BUILD
        ↓
      CHECK
        ↓
      STATE


Is the user asking about project status?
        │
       YES
        ↓
      STATE / project_state


Is something broken?
        │
       YES
        ↓
   Retrieve relevant code
        ↓
      CHECK
        ↓
      BUILD fix
        ↓
      CHECK again
```

---

# 10. Vertical Slice Development

Prefer building FloodLens features end-to-end in small vertical slices.

Example:

```text
Data
 ↓
Feature Engineering
 ↓
Model
 ↓
API
 ↓
Frontend
 ↓
Visualization
```

For example, instead of implementing the entire ML system first:

```text
Zone data
 ↓
Feature extraction
 ↓
Baseline prediction
 ↓
/zones/{id}/prediction
 ↓
Zone Details Panel
```

Then expand the system.

This keeps the application continuously demonstrable.

---

# 11. ML Agent Responsibilities

The agent must preserve the project's ML structure:

```text
Data
 ↓
Preprocessing
 ↓
Logistic Regression
 ↓
ANN
 ↓
Evaluation
 ↓
Prediction
 ↓
SHAP
 ↓
Confidence
 ↓
Spatial Error Analysis
```

Do not introduce unnecessary ML complexity.

The ANN should remain appropriate for tabular geographic features.

Never fabricate:

- Training data
- Flood incidents
- Metrics
- Model performance
- SHAP values
- Confidence values

---

# 12. Geospatial Agent Responsibilities

Any geospatial implementation must explicitly consider:

```text
CRS
Geometry
Spatial joins
Distance
Area
Coordinate accuracy
```

Before spatial operations:

```text
Check CRS
   ↓
Reproject if required
   ↓
Validate geometry
   ↓
Perform operation
   ↓
Validate result
```

Do not invent geographic data.

---

# 13. Frontend Agent Responsibilities

The frontend should maintain the intended flow:

```text
3D Globe
   ↓
India
   ↓
Hyderabad
   ↓
Study Area
   ↓
Risk Layer
   ↓
Zone
   ↓
Zone Intelligence
```

Use:

- CesiumJS for global/3D navigation
- MapLibre for detailed spatial visualization

Prefer reusable components over a single large page.

---

# 14. Scenario Feature

Scenario simulation is optional.

If implemented:

```text
Select Zone
    ↓
Modify Input
    ↓
Run Model
    ↓
Compare Prediction
    ↓
Explain Difference
```

Always describe the result as:

> Model susceptibility under a hypothetical scenario.

Never convert the result into a claim about actual future flooding.

---

# 15. Architecture Change Protocol

Do not replace an existing technology simply because another technology is newer or more popular.

Before a major architecture change:

```text
Current approach
      ↓
Problem
      ↓
Evidence
      ↓
Proposed change
      ↓
Affected modules
      ↓
Implementation
      ↓
Validation
      ↓
Update project_state.md
```

Major architecture changes should require clear justification.

---

# 16. Dependency Rule

Before adding a dependency ask:

```text
Does the project actually need it?
        │
       NO → Do not add it
        │
       YES
        ↓
Can existing dependencies solve it?
        │
       YES → Reuse them
        │
       NO
        ↓
Add the smallest appropriate dependency
```

Avoid unnecessary:

- LLMs
- RAG
- Vector databases
- Agent frameworks
- Multi-agent systems
- Kafka
- Redis
- Kubernetes
- Microservices

unless a concrete requirement justifies them.

---

# 17. Definition of Done

A task is complete when:

```text
Implementation complete
        +
Relevant tests pass
        +
No critical regression
        +
Interfaces/types are correct
        +
Documentation/state updated
```

Do not claim completion based solely on generated code.

---

# 18. Final Rule

The agent should optimize for:

```text
Correctness
    ↓
Data integrity
    ↓
Reproducibility
    ↓
Maintainability
    ↓
Explainability
    ↓
Performance
    ↓
Visual polish
```

The goal is not to build the largest architecture.

The goal is to build the **smallest technically credible FloodLens system that fully demonstrates the problem, model, explainability, geographic intelligence, and planning value.**
```

