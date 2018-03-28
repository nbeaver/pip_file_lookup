all :
	./pip_file_lookup.py $(HOME)/.local/lib/python3.5/site-packages/requests/__init__.py

profile :
	python3 -m cProfile -o out.prof pip_file_lookup.py $(HOME)/.local/lib/python3.5/site-packages/requests/__init__.py
