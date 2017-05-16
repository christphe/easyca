init:
	pip3 install -r requirements.txt

test:
	py.test tests

clean:
	rm -rf ./dist
	@test -f ".cid" && docker rm -f `cat .cid` && rm -f .cid && echo "Removed container" || echo "No container to remove"
all:
	pyinstaller -F easyca/easyca.py

install:
	cp ./dist/easyca /usr/bin/easyca
	chmod +x /usr/bin/easyca

.PHONY: init test