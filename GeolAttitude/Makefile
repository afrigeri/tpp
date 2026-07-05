PLUGINNAME = GeolAttitude

CURR_DIR=tpp

zip:
	black *.py
	cd .. && make tests
	cd .. && zip -r $(PLUGINNAME).zip $(PLUGINNAME) -x "*.pyc" "*__pycache__*" ".git"
