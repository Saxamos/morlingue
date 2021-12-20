.PHONY: setup_env
setup_env: clean
	virtualenv -p python3 venv
	. venv/bin/activate; pip install -e .

.PHONY: run_prod
run_prod: setup_env
	. venv/bin/activate; nohup run_backend &
	. venv/bin/activate; nohup run_frontend &
	. venv/bin/activate; nohup streamlit run bff/frontend.py &

.PHONY: check_type_format
check_type_format:
	mypy --config-file=./mypy.ini .
	isort .
	black .

.PHONY: tests
tests:
	python -u -m pytest tests -vv

.PHONY: clean
clean : ## remove all transient directories and files
	rm -rf venv
	rm -rf *.egg-info
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$|.pytest_cache|.mypy_cache)" | xargs rm -rf
