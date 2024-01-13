# Cooleans

Cooleans is a Python package that aims to enhance the bool type in Python by adding a new possible value: "perhaps". This is a value that is neither True nor False, but rather may be one of those values. With cooleans, you can more accurately represent situations where the truth value of a statement is uncertain or unknown.

## Getting Started

### Installation

You can install cooleans using pip:  
`pip install cooleans`

### Usage

Here's an example of how to use cooleans in Python:

```python
from cooleans import DefinitelyTrue, DefinitelyFalse, Perhaps

my_bool = DefinitelyTrue
if my_bool:
    print("This is definitely true")

my_bool = Perhaps
if my_bool >= Perhaps:
    print("This might be true")
```

In this example, we create a `DefinitelyTrue` coolean value and use it in an if statement to print "This is definitely true". We then create a Perhaps coolean value and use it in an if statement to print "This might be true". Note that Perhaps will always have a truth value of False when treated as a bool.  

### Supported Operators

Cooleans support the same logical operators as normal bools in Python, including:

- `and`
- `or`
- `not`
- `==`
- `!=`
- `<`
- `>`
- `<=`
- `>=`

### Using Values Directly

Cooleans can be used directly as values since they are implemented as a Python class, like so:

```python
from cooleans import DefinitelyTrue, DefinitelyFalse, Perhaps

print(DefinitelyTrue and DefinitelyFalse)
```

This code snippet will output DefinitelyFalse.  

## Contributing

We don't welcome contributions to cooleans yet.  

## License

This project is licensed under the MIT License - see the LICENSE file for details.  
