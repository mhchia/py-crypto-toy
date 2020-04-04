PKG = crypto_toy
TESTS = tests
SETUPPY = setup.py

format:
	black $(PKG) $(TESTS) $(SETUPPY)
	isort --recursive $(PKG) $(TESTS) $(SETUPPY)

lint: format
	black --check $(PKG) $(TESTS) $(SETUPPY)
	isort --recursive --check-only $(PKG) $(TESTS) $(SETUPPY)
	flake8 $(PKG) $(TESTS) $(SETUPPY)
	mypy -p $(PKG) --config-file mypy.ini
