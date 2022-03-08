.PHONY: setup_env
setup_env: clean
	pip install -e .

.PHONY: run_prod
run_prod: setup_env
	nohup run_backend &
	nohup run_frontend &
	nohup streamlit run bff/frontend.py &

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
