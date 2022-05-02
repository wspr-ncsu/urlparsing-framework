#!/bin/sh

# delete existing files
rm /home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/*.json

# python urllib3
nox --noxfile /home/dashmeetkaur/Desktop/urlparse/url-parsing/libs/urllib3/noxfile.py --reuse-existing-virtualenvs --sessions test-3.9 -- test/test_util.py::TestUtil

# python urllib
make -C '/home/dashmeetkaur/Desktop/urlparse/url-parsing/libs/cpython/' test TESTOPTS="-v test_urlparse"

# php
php /home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/extract_php_url.phpt