
SRC := ./src/
BIN := ./bin/

NAME := mandelbrot


.PHONY: build clean

build: $(BIN)$(NAME)

clean:
	rm -rf $(BIN)


$(BIN)$(NAME): $(SRC)$(NAME).fut
	mkdir -p $(BIN)
	futhark multicore $^ -o $@
