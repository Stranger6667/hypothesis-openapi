default:
    @just --list

# Quick aliases
alias c := check
alias f := fmt
alias t := test
alias tc := test-cov

# Run all tests
test *ARGS:
    python -m pytest {{ARGS}}

# Run tests with coverage
test-cov *ARGS:
    @rm -f .coverage*
    coverage run -m pytest {{ARGS}}
    coverage combine
    coverage report

# Run tests matching pattern
test-k PATTERN *ARGS:
    python -m pytest -k "{{PATTERN}}" {{ARGS}}

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
