.PHONY: help prepare-dev clean lint test build

help:
	@echo "  \033[1mhelp\033[0m         - print this message"
	@echo "  \033[1mprepare-dev\033[0m  - setup pipenv and install dependencies"
	@echo "  \033[1mclean\033[0m        - remove artifacts"
	@echo "  \033[1mlint\033[0m         - run linters"
	@echo "  \033[1mtest\033[0m         - run tests"
	@echo "  \033[1mpackage\033[0m      - package submittable artifacts"
	@echo "  \033[1mbuild\033[0m        - clean -> lint -> test -> package"

prepare-dev:
	@echo "\033[1mprepare-dev\033[0m"
	which pipenv > /dev/null || exit 2
	pipenv install --dev

clean:
	@echo "\033[1mclean\033[0m"
	rm -rf .mypy_cache/ .pytest_cache/ htmlcov/ .coverage
	rm -rf build/ dist/
	find . -name '*.pyc' -exec rm -rf {} +

lint:
	@echo "\033[1mlint\033[0m"
	@echo "\033[1mlint:flake8\033[0m"
	pipenv run flake8 src/ tests/
	@echo "\n\033[1mlint:pylint\033[0m"
	pipenv run pylint --rcfile=setup.cfg src/* tests/*
	@echo "\033[1mlint:mypy\033[0m"
	pipenv run mypy src/ tests/

test:
	@echo "\033[1mtest\033[0m"
	PYTHONPATH=${PYTHONPATH}:./src pipenv run pytest tests/

package:
	@echo "\033[1mpackage\033[0m"
	which zip > /dev/null || exit 2
	rm -rf build dist && mkdir build dist
	cd src && zip -x main.py -r ../dist/packages.zip . && cp main.py ../dist
	cd ..
	pipenv lock -r | pipenv run pip install -U -r /dev/stdin -t build/libs
	cd build/libs && pwd && ls && zip -r ../../dist/libs.zip .

build: clean lint test package
