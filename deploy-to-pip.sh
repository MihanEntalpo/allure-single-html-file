

rm -rf dist build *.egg-info

python setup.py install
python setup.py sdist bdist_wheel
twine upload dist/* --verbose

rm -rf dist build *.egg-info
