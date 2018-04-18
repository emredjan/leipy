.PHONY: clean

PROJECT := leipy
TEST_PATH=./

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf $(PROJECT).egg-info

test: clean-pyc
	pytest $(TEST_PATH)

build-sdist: clean
	python setup.py sdist

build-bdist: clean
	python setup.py bdist_wheel

upload:
	twine upload dist/*