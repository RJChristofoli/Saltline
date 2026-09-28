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

Saltline is in early development. The [v0.1 architecture](docs/adr/0001-v01-technical-architecture.md) is defined, and the Python package and CLI foundation are available. Repository analysis commands are planned but not yet implemented.

## Local setup

Requires Python 3.11 or newer. From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
saltline --help
saltline --version
python -m pytest
```

The package has no runtime dependencies. The optional `dev` extra installs test and package-build tools. `python -m saltline` also runs the CLI.

## Contributing

Saltline uses GitHub Issues, milestones, pull requests, and a public project board to plan and track development. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and [docs/project-workflow.md](docs/project-workflow.md) for the reasoning behind it.

## License

Saltline is available under the [MIT License](LICENSE).
