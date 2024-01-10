install: install-flit
	flit install --deps develop

develop: install-flit
	flit install --deps all --pth-file

install-flit:
	python -m pip install --upgrade pip
	pip install flit

format:
	ruff format .\arcGisFeatureCash\

typecheck:
	mypy .\arcGisFeatureCash\


# todo: make sure in production covar is at least 90%
test:
	pytest --cov=arcGisFeatureCash/ --cov-report=term-missing --cov-fail-under=40

bumpversion-major:
	bumpversion major

bumpversion-minor:
	bumpversion minor

bumpversion-patch:
	bumpversion patch

bumpversion-build:
	bumpversion build
	
build-wheel:
	flit build

docs-serve:
	mkdocs serve

docs-publish:
	mkdocs build
# 	mkdocs gh-deploy
