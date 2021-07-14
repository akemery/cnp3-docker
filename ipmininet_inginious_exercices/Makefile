ROOT_DIR="."
BATS_PATH="./bats/bats/bin"
TEST_PATH="./tests"
.PHONY: test

default: bats test clean

bats:
	git clone https://github.com/bats-core/bats-core.git $(ROOT_DIR)/bats/bats
	git clone https://github.com/bats-core/bats-support.git $(ROOT_DIR)/bats/test_helper/bats-support
	git clone https://github.com/bats-core/bats-assert.git $(ROOT_DIR)/bats/test_helper/bats-assert

test:
	pytest-3 tests
	$(BATS_PATH)/bats $(TEST_PATH)/
	
clean:	  
	rm *.txt
