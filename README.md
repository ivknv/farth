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

### Arithmetic operations ###
```forth
5 3 + print # Will display 8
4 5 - print # Will display 1
5 4 * print # Will display 20
2 10 / print # Will display 5
10 % 5 print # Will display 0
```

### Stack manipulation ###
There's not a lot of words for stack manipulations.<br/>

```dup``` - duplicates last value on the stack<br/>
```.``` - removes last value from stack<br/>
