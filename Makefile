DIST_DIR=./dist

build:
	mkdir -p $(DIST_DIR)
	hy2py3 long-cmd-notify.hy > $(DIST_DIR)/long-cmd-notify.py
