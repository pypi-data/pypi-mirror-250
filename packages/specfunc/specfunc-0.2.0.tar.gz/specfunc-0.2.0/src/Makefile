# Configuration

FC := gfortran
LD := $(FC)
RM := rm -f

# Source files
SRCS := special_functions.f90
PROG := special_functions
OBJS := $(addsuffix .o, $(SRCS))

# Library
LIB := pylib.f90

.PHONY: all clean
all: $(PROG)

$(PROG): $(OBJS)
	$(LD) -o $@ $^

$(OBJS): %.o: %
	$(FC) -c -o $@ $<

lib: $(OBJS)
	$(FC) -c $(SRCS)
	$(FC) -m64 -shared $(LIB) -o $(PROG).so $(OBJS)

clean:
	$(RM) $(filter %.o, %(OBJS)) $(wildcard *.mod) $(PROG) $(wildcard *.so)
