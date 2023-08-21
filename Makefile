.PHONY: linters test test-all

linters:
	flake8 mbc2 tests
	mypy

test:
	pytest

test-all: linters test
