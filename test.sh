pytest -s --cov=Automate ./test.py

coverage html
firefox htmlcov/Automate_py.html

