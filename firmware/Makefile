CXX ?= g++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror
CPPFLAGS ?= -Iinclude

BUILD_DIR := build/host
SOURCES := \
	src/controller.cpp \
	src/inputs.cpp \
	src/joystick.cpp \
	src/nextion.cpp \
	src/router.cpp \
	src/visca.cpp
TEST_BINARY := $(BUILD_DIR)/ptz_tests

.PHONY: all test

all: $(TEST_BINARY)

$(TEST_BINARY): $(SOURCES) tests/test_main.cpp
	mkdir -p $(BUILD_DIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $^ -o $@

test: $(TEST_BINARY)
	./$(TEST_BINARY)
