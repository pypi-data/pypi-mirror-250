venv:
	python3.10 -m venv .venv
	echo 'run `source .venv/bin/activate` to start develop FlowTask'

install:
	pip install --upgrade pip
	pip install wheel==0.42.0
	pip install --upgrade asyncdb[all]
	pip install --upgrade navigator-api
	pip install --upgrade navigator-session
	pip install --upgrade navigator-auth
	pip install --upgrade async-notify[all]
	pip install --upgrade querysource
	# dev
	python -m pip install -Ur docs/requirements-dev.txt
	# Install extra resources
	pip install --upgrade qworker
	# install FlowTask
	pip install -e .
	echo 'start develop FlowTask'

compile:
	python setup.py build_ext --inplace

dev:
	flit install --symlink

release: lint test clean
	flit publish

format:
	python -m black flowtask

distclean:
	rm -rf .venv
