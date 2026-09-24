# Saltline

**Architecture intelligence for safer software changes.**

Saltline analyzes source code, Git history, tests, ownership, and architectural rules to identify the parts of a codebase where change is most likely to cause regressions.

The project is inspired by the idea of a protective salt line: explicit boundaries that reveal and contain architectural risk.

## Vision

Saltline connects signals that are usually analyzed in isolation:

- source structure and dependencies;
- complexity and code churn;
- change coupling and ownership;
- test protection;
- architectural boundaries and drift;
- agent-assisted investigation and refactoring.

The long-term goal is to provide coding agents with enough repository intelligence to explain risks, plan safe changes, implement refactors, and verify the result.

## Planned workflow

```bash
saltline analyze .
saltline explain path/to/hotspot.py
saltline plan-refactor path/to/hotspot.py
saltline guard --architecture
```

## Initial scope

The first version will focus on deep support for Python/Django and TypeScript/React repositories, including:

- Git history ingestion;
- Python AST analysis;
- import and symbol graphs;
- complexity, churn, and change-coupling metrics;
- architecture rules defined in `.saltline.yml`;
- local reports and repository-level risk analysis.

## Status

Saltline is in the earliest stage of development. The architecture and first vertical slice are currently being designed.

## License

Saltline is available under the [MIT License](LICENSE).
