Tutorial
========

Create and Test a C component 
-----------------------------

Why not start with a simple example. With your favourite text editor, create a
file count.c and add the following::
        
        void main(){
                int i;
                for(i=1; i<=10; i++){
                        report(i);
                }
        }

You can convert C components into Verilog components using the C2Verilog
compiler. The verilog output is *test.v* file. The *iverilog* option causes the generated Verilog component to be
compiled using Icarus Verilog. The *run* option causes simulation to be run::

        ~$ c2verilog iverilog run test.c
          1 (report (int) at line: 5 in file: /home/ben/test.c)
          2 (report (int) at line: 5 in file: /home/ben/test.c)
          3 (report (int) at line: 5 in file: /home/ben/test.c)
          4 (report (int) at line: 5 in file: /home/ben/test.c)
          5 (report (int) at line: 5 in file: /home/ben/test.c)
          6 (report (int) at line: 5 in file: /home/ben/test.c)
          7 (report (int) at line: 5 in file: /home/ben/test.c)
          8 (report (int) at line: 5 in file: /home/ben/test.c)
          9 (report (int) at line: 5 in file: /home/ben/test.c)
         10 (report (int) at line: 5 in file: /home/ben/test.c)
        /home/ben/test.v:308: $finish called at 4675 (1s)

When a design is reset, execution starts with the *main* function defined in
the C file. The C program will
appear to execute in sequence, although the compiler may execute instructions
concurrently if it does not affect the outcome of the program. This will allow
your component to take advantage of the inherent parallelism present in a hardware
design.

The *report* function is a *built-in* function which is helpful for debug, it
will print the value of a variable on the console during simulations, when you
synthesise the design it will be ignored.

This component doesn't have any inputs or outputs, so it isn't going to be very
useful in a real design. You can add inputs and outputs to a components using
streams. Open streams with *input* or *output* calls with stream names. Read from
streams using *fgetc* and write to stream using *fputc*.

::

        unsigned spam = input("spam");
        unsigned eggs = input("eggs");
        unsigned fish = input("fish");
        int temp;
        temp = fgetc(spam); //reads from an input called spam
        temp = fgetc(eggs); //reads from an input called eggs
        fputc(temp, fish);   //writes to an output called fish


Reading or writing from inputs and outputs causes program execution to block
until data is available. This synchronises data transfers with other components
executing in the same device, this method of passing data between concurrent
processes is much simpler than the mutex/lock/semaphore mechanisms used in
multithreaded applications.

If you don't want to commit yourself to reading and input and blocking
execution, you can check if data is ready::

        int temp;
        if(ready(spam)){
                temp = fgetc(spam);
        }

There is no equivalent function to check if an output is ready to receive data,
this could cause deadlocks if both the sending and receiving end were waiting
for one another.

We can now construct some basic hardware components quite simply. Here's a counter for instance::

        void counter(){
                while(1){
                        for(i=1; i<=10; i++){
                                fputc(i, out);
                        }
                }
        }

We can generate an adder like this::

        void added(){
                while(1){
                        fputc(fgetc(a) + fgetc(b), z);
                }
        }

Or a divider like this (yes, you can synthesise division)::

        void divider(){
                while(1){
                        fputc(fgetc(a) / fgetc(b), z);
                }
        }

We can split a stream of data into two identical data streams using a tee function::

        void tee(){
                int temp;
                while(1){
                        temp = fgetc(a);
                        fputc(temp, y);
                        fputc(temp, y);
                }
        }

If we want to merge two streams of data, we could interlace them::

        void interlace(){
                int temp;
                while(1){
                        temp = fgetc(a);
                        fputc(temp, z);
                        temp = fgetc(b);
                        fputc(temp, z);
                }
        }

or we could prioritise one stream over the other::

        void arbiter(){
                int temp;
                while(1){
                        if( ready(a) ){
                                temp = fgetc(a);
                                fputc(temp, z);
                        } else if( ready(b) ){
                                temp = fgetc(b);
                                fputc(temp, z);
                        }
                }
        }

