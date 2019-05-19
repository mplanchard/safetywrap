VENV = . ./venv/bin/activate;
TEST = pytest --cov-config=setup.cfg --cov=result_types tests
LINE_LENGTH = 79

.PHONY: clean build fmt lint test

all: fmt lint test

venv: venv/bin/activate
venv/bin/activate: setup.py
	python3 -m venv venv
	$(VENV) pip install -e .[dev]
	touch venv/bin/activate

build: venv
	$(VENV) python setup.py sdist bdist_wheel

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

fmt: venv
	$(VENV) black --line-length $(LINE_LENGTH) *.py src tests

lint: venv
	$(VENV) pylama src tests
	$(VENV) mypy src tests
	$(VENV) black --check --line-length $(LINE_LENGTH) src tests

test: venv
	$(VENV) $(TEST)

test-3.6:
	docker run --rm -it --mount type=bind,source="$(PWD)",target="/src" -w "/src" \
		python:3.6 bash -c "make clean && pip install -e .[dev] && $(TEST); make clean"

test-3.7:
	docker run --rm -it --mount type=bind,source="$(PWD)",target="/src" -w "/src" \
		python:3.7 bash -c "make clean && pip install -e .[dev] && $(TEST); make clean"

test-3.8-rc:
	docker run --rm -it --mount type=bind,source="$(PWD)",target="/src" -w "/src" \
		python:3.8-rc bash -c "make clean && pip install -e .[dev] && $(TEST); make clean"

test-all-versions: test-3.6 test-3.7 test-3.8
