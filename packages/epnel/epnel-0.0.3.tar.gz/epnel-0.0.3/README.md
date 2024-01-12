# epnel
A simple esoteric and lispy programming language without parentheses.

## description
### operators
Each operator takes two arguments: (expression, expression).
They work the way you would expect.
 - `+` - addition
 - `-` - subtraction
 - `*` - multiplication
 - `/` - division
 - `<` - comparison (lower than)
 - `>` - comparison (bigger than)
 - `|` - alternation (or)
 - `^` - disjunction (xor)
 - `&` - conjunction (and)
 - `=` - equation (is equal to?)

> Comparison operators return boolean types.

> Logical operators work either on number's bits or booleans.

### conditionals
Conditional takes three arguments: (test, then, else).
If "test" evaluates to True, then the "then" branch is executed. Otherwise the "else" branch is executed.
 - `?` - conditional

### assignments
The first argument for each assignment operator is a name.
Names are also expressions and will be evaluated before assignment.
The only restriction is that you can't bind to any reserved keywords.
 - `.` - variable assignment
 - `,` - function assignment
 - `:` - number reassignment

The variable assignment takes two arguments: (name, expression).
"Expression" is evaluated and it's value is bound to the name.

The function assignment takes three arguments: (name, definition, expression).
"Definition" is an expression, which isn't evaluated until the "name" is called.
Whenever a call to "name" appears it will evaluate the function definition expression and return it's new value.
"Expression" is the return value of the function assignment.

> Assignments bind values or expressions to names. This means you can also change the behaviour of numbers.

Number reassignment takes only one argument and returns a value of it's argument's value. Similar functionality is attributed to "dereference" in some languages. The argument is interpreted as if it's value was typed straight in place of this assignment.

> Number reassignment reassigns to itself a number corresponding to the value of it's name.

### booleans
You can produce booleans using comparison operators. True is equal to 1 and False is equal to 0.
The boolean primitive evaluates to False (and is immutable).
 - `!` - boolean (false)

### numbers
or as some would say: literals
#### decimals
Decimal numbers are composed of digits or passed around as variables.
The default value for any variable is zero: 0 or False.

#### names
The variable name can be anything which is not a language keyword.
If name is an expression it is evaluated and the result is used as a literal name.
You can use the assignment to bind names with values.

### expressions
Expressions are evaluated either to numbers or booleans. Everything is an expression.

## inspiration
[Polish Notation](https://pl.wikipedia.org/wiki/Notacja_polska) was the inspiration to write this language, therefore I named the language "epnel".
```
E - Esoteric
P - Polish
N - Notation
E - Evaluation
L - Language
```

## installation
You can simply use:
```
$ pip install .
```

## wishlist
Some things that might be nice to have:
 - compiler to C

## license

GNU GPLv3

