farth
=====

Forth-like programming language

## Installation ##
Run ```python setup.py install```<br/>
After that You will be able to run interpreter by running following command:
```bash
python -m Farth
```

## Syntax ##
Syntax is almost the same as in typical Forth language.

### Hello world ###
```forth
"Hello, world!" print
```

### Comments ###
There's ```#``` for word commenting everything after it on the same line.
Example:
```forth
# This is a comment
# 123 print
```

### Arithmetic operations ###
```forth
5 3 + print # Will display 8
4 5 - print # Will display 1
5 4 * print # Will display 20
2 10 / print # Will display 5
10 % 5 print # Will display 0
```

### Custom words ###
```:``` word starts word definition and ```;``` ends it.<br/>
Example:
```forth
: plus + ;
: plus10 10 plus ;
8 plus10 print # Will display 18
```

Words are more like macros.<br/>
For example, You can define word that defines another word.

### Stack manipulation ###
```dup``` - (n -- n n) duplicates last value on the stack<br/>
```drop``` - (n -- ) removes last value from stack<br/>
```over``` - (n1 n2 -- n1 n2 n1) duplicates previous value<br/>
```rot``` - (n1 n2 n3 -- n2 n3 n1) 'rotates' 3 last values<br/>
```swap``` - (n1 n2 -- n2 n1) swaps 2 last values<br/>
```2dup``` - (d -- d d) duplicates last pair of values<br/>
```2drop``` - (d -- ) removes last pair of values<br/>
```2swap``` - (d1 d2 -- d2 d1) swaps 2 last pairs of values<br/>
```2over``` - (d1 d2 -- d1 d2 d1) duplicates previous pair of values<br/>
```.s``` - print current stack contents

### Branching ###
```1``` means ```true```. Any other value means ```false```.<br/>
The following example defines a new word that prints "true" if condition is true and "false" if it's false:
```forth
: testif if "true" print else "false" print endif ;
0 testif # "false"
1 testif # "true"
```

### Loops ###
Farth ```loop``` are similiar to while loop.
First, You have to put value on the ```loop stack```:
```forth
1 do "Something" print loop # WARNING: this loop will run forever!
0 do "nothing" print loop # Will print only once
```

You can use ```la``` word to put values on loop stack.
