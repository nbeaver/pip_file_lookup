Matches filepaths to pip package.

Example usage::

    $ pip3 install --user requests
    $ # Absolute path.
    $ pip_file_lookup.py ~/.local/lib/python3.6/site-packages/requests/__init__.py
    requests
    $ pip3 install --user six
    $ # Relative path.
    $ pip_file_lookup.py .local/lib/python3.6/site-packages/six.py
    six
