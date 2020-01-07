install:
	pip3 install -e .

package:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*