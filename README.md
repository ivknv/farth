farth
=====

[Forth](http://wikipedia.org/wiki/Forth_(programming_language))-like programming language written in Python (which is not recommended for these things as any other scripting language).</br>

You can guess everything about Farth by thinking of its name...

## Table of contents ##
1. [Installation](#installation)
2. [Syntax](#syntax)
3. [Hello world](#hello-world)
4. [Comments](#comments)
5. [Arithmetic operations](#arithmetic-operations)
6. [Comparison](#comparison)
7. [Custom words](#custom-words)
8. [Stack manipulation](#stack-manipulation)
9. [Branching](#branching)
10. [Loops](#loops)
11. [Includes](#includes)

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

### Comparison ###
Comparison operators are the same as in typical Forth.<br/>
```=``` - equal<br/>
```!=``` - not equal<br/>
```<=``` - less or equal<br/>
```>=``` - greater or equal<br/>
```<``` - less<br/>
```>``` - greater<br/>

If condition is true it will push ```1``` to the stack or ```0``` if it's false.

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
Farth ```loop``` is similiar to loop in Forth.
You have to put value on the ```loop stack``` with ```do```, right after that write some code to be repeated and call ```loop``` word<br/>
The following example prints digits from 10 to 1:
```forth
10 do i print loop
```

```i``` copies current value from loop stack and pushes it to the data stack.<br/>

You can use ```la``` word to put values on loop stack.

### Includes ###
You can include Farth code into Your program from files.<br/>
To do that You can use ```include``` as in following example:
```forth
"some_file.forth" include
```

This will execute code from ```some_file.forth```.

**Note**: include is not the same as import.
