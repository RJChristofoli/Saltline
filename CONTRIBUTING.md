# Contributing to Saltline

Saltline is developed in small, reviewable increments. Every change should start from a GitHub issue and finish with evidence that its acceptance criteria were met.

## Workflow

1. Select an issue from the project board.
2. Confirm that the issue has clear acceptance criteria and no unresolved dependencies.
3. Move it to **Ready**, then to **In progress** when work begins.
4. Create a branch from `main` using `issue-<number>/<short-description>`.
5. Keep commits focused and use Conventional Commits.
6. Open a pull request that links the issue with `Closes #<number>`.
7. Record tests, design decisions, and relevant limitations in the pull request.
8. Move the item to **In review**. Merge only after checks pass and the acceptance criteria are satisfied.
9. Move the item to **Done** after the pull request is merged.

## Definition of Ready

An issue is ready when:

- its problem and expected outcome are clear;
- acceptance criteria are testable;
- dependencies and relevant technical risks are identified;
- it is small enough to complete in one focused pull request.

## Definition of Done

A change is done when:

- the acceptance criteria are satisfied;
- automated tests cover the behavior where appropriate;
- documentation is updated when behavior or architecture changes;
- quality checks pass;
- the pull request explains important decisions and tradeoffs;
- no known critical regression remains.

## Branches and commits

Branch examples:

```text
issue-12/python-ast-parser
issue-18/hotspot-ranking
```

Commit examples:

```text
feat: extract Python symbols from AST
fix: handle commits without an author email
docs: explain hotspot scoring
test: cover cyclic import detection
```

## Pull requests

Prefer small pull requests with one primary purpose. If implementation reveals a separate concern, create another issue instead of silently expanding the scope.

Architectural decisions that are difficult to reverse should be captured as an ADR in `docs/adr/`.
