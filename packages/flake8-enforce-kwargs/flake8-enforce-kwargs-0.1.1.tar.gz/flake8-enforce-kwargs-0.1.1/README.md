flake8-enforce-kwargs
=======================

Overview
--------

`flake8-enforce-kwargs` is a Flake8 plugin designed to enforce the use of keyword arguments in functions and class methods. This plugin helps promote code clarity and readability by encouraging the explicit naming of arguments, making it easier for developers to understand the purpose of each parameter.

Installation
------------

To install the `flake8-enforce-kwargs` plugin, use the following pip command:


`pip install flake8-enforce-kwargs`

Usage
-----

After installation, runs automatically when you run the flake8 command.
For example:


```flake8 your_project_directory```

This will check your Python files for functions and class methods that do not use keyword arguments. Any violations of the rule will be reported in the Flake8 output.

Configuration
-------------

The plugin can be configured using the Flake8 configuration file (usually setup.cfg or .flake8). Add the following section to enable and configure the `flake8-enforce-kwargs` plugin:


Additionally, you can customize the behavior of the plugin by adjusting the following optional settings:

-   exclude: A list of names or patterns for functions or methods to exclude from the keyword argument check.

Example configuration:


```[flake8]
per-file-ignores =
    utils.py:EKW002,EKW001
````
Rules
-----

The `flake8-enforce-kwargs` plugin enforces the following rules:

All arguments in functions and class methods must use keyword arguments.

Example
-------

pythonCopy code

```# flak8: noqa

# This function violates the rule
def add(x, y):
    return x + y

# This class method violates the rule
class Calculator:
    def multiply(self, a, b):
        return a * b
```

In the example above, the `add` function and the `multiply` method violate the keyword argument rule. Running Flake8 with the `flake8-enforce-kwargs` plugin will report these violations.

License
-------

`flake8-enforce-kwargs` is licensed under the MIT License - see the LICENSE file for details.