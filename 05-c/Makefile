CC     = gcc
CFLAGS = -g -O0 -Wall

SRCS = $(wildcard exercises/*.c)
BINS = $(SRCS:.c=)

all: $(BINS)

exercises/%: exercises/%.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(BINS)
