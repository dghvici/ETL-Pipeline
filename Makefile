PROJECT_NAME = NC-DataEng-ETL-Project
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip
GIT:=git
REGION = eu-west-2

# Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute python related functionalities from within the project's environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

# Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)
	$(call execute_in_env, $(PIP) install -r ./requirements_lambda.txt -t modules/python)
	$(call execute_in_env, $(GIT) clone https://github.com/jkehler/awslambda-psycopg2.git)
	$(call execute_in_env, cp -r awslambda-psycopg2/psycopg2-3.11/* modules/python/)
	$(call execute_in_env, $(PIP) install -r ./requirements_transform.txt -t modules_transform/python)

# Run the security test (bandit)
security-test:
	$(call execute_in_env, bandit -lll ./src/*.py ./test/*.py \
	./util_func/*.py ./test_utils/*.py)

# Run pip-audit test
audit-test:
	$(call execute_in_env, pip-audit)

# Run the black code check
run-black:
	$(call execute_in_env, black --line-length 79 ./src/*.py ./test/*.py \
	./util_func/*/*.py ./test_utils/*.py)

# Run docformatter
run-docformatter:
	$(call execute_in_env, docformatter --in-place --wrap-summaries \
	79 --wrap-descriptions 79 ./src/*.py ./test/*.py \
	./util_func/*/*.py ./test_utils/*.py)

# Run flake8
run-flake8:
	$(call execute_in_env, flake8 ./src/*.py ./test/*.py \
	./util_func/*/*.py ./test_utils/*.py)

# Run the unit tests
unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest ./test/*.py  ./test_utils/*.py )

# Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=src test/)
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest --cov=util_func test_utils/)

# Run security tests
run-security: security-test audit-test


# Run formatting and tests
run-checks: run-black run-docformatter run-flake8 unit-test check-coverage

# Run all
run-make: requirements run-security run-checks