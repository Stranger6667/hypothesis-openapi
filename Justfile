default:
    @just --list

# Quick aliases
alias c := check
alias f := fmt
alias t := test
alias tc := test-cov

# Run all tests
test *ARGS:
    python -m pytest tests/ {{ARGS}}

# Run tests with parallelism
test-dist *ARGS:
    python -m pytest tests/ -n auto {{ARGS}}

# Run tests with coverage
test-cov *ARGS:
    @rm -f .coverage*
    COVERAGE_PROCESS_START=pyproject.toml coverage run -m pytest tests/ -n auto {{ARGS}} || true
    coverage combine
    coverage report

# Run tests matching pattern
test-k PATTERN *ARGS:
    python -m pytest tests/ -k "{{PATTERN}}" {{ARGS}}

check:
    uvx prek run --all-files

fmt:
    uvx prek run ruff-format --all-files

lint:
    uvx prek run ruff-check --all-files

fix:
    uvx ruff check --fix src/ tests/

typecheck:
    uvx prek run mypy --all-files

clean-cov:
    rm -f .coverage* coverage.xml
