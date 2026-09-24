# Saltline project workflow

This document explains how Saltline uses GitHub as an engineering system rather than only as source control.

## Planning hierarchy

- **Roadmap:** the product direction described in the README and project board.
- **Milestone:** a coherent, demonstrable version such as `v0.1.0 — Repository Intelligence`.
- **Issue:** one observable outcome that can normally be delivered in a single pull request.
- **Pull request:** the implementation, validation evidence, and review discussion for an issue.
- **Commit:** one meaningful step inside a pull request.

## Board stages

- **Backlog:** valuable work that is not yet prepared or scheduled.
- **Ready:** refined work that can be started without another planning decision.
- **In progress:** actively being implemented. Keep this column small.
- **In review:** a pull request exists and is awaiting checks or review.
- **Done:** merged work whose acceptance criteria were verified.

The suggested work-in-progress limit is one item in **In progress** and one item in **In review** while Saltline has a single maintainer. This makes blocked work visible and encourages completing changes before starting more.

## Labels

Labels answer four different questions:

- `type:*` — what kind of work is this?
- `area:*` — which part of Saltline does it affect?
- `priority:*` — how important is it relative to other work?
- `size:*` — how much uncertainty and effort does it contain?

Board status should not be duplicated as a label because the project field already owns that information.

## Milestones and releases

A milestone should end in a demonstrable capability, not simply a date. The initial sequence is:

1. `v0.1.0 — Repository Intelligence`: ingest a repository and rank explainable hotspots.
2. `v0.2.0 — Architecture Guard`: define boundaries and detect architectural drift.
3. `v0.3.0 — Agent Workflows`: produce grounded explanations and safe refactoring plans.

## Issue quality

A good issue describes the problem before the implementation. It includes:

- context and motivation;
- a concrete outcome;
- testable acceptance criteria;
- dependencies or explicit non-goals;
- technical notes only when they constrain the solution.

Research issues should finish with a decision or artifact. They are not open-ended invitations to explore.

## Pull request quality

A pull request should make review inexpensive. It should explain:

- what changed and why;
- how the change was validated;
- which issue it closes;
- what was intentionally left out;
- whether it introduces an architectural decision or follow-up work.
