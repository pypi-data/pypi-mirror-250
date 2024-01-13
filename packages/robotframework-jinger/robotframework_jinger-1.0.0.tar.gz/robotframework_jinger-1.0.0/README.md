# JingeR: Jinja generator for Robot Framework

Generate data-driven Robot Framework testcases using Jinja templates.

## Use Cases

- Generate tests for a REST API 
- Static test generation (as opposed to dynamic test generation using the [Listener interface](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface))

## How to use it

1. Install the package

```bash
pip install robotframework-jinger
```

2. Save the default template to the current directory


```bash
jinger init
```

**Hint**: In case your environment does not allow executing jinger, call the Python module directly:

```bash
python -m JingeR init
```

3. Modify the template and the testdata

**Notes**

- Each RF variable in the template that should be replaced by its value must be named according to the following pattern: `${T_foo}`.
- The template file is a valid .robot file in order to allow testing the template test case without having to first run Jinja to process the file. 

4. Generate a Robot Framework testsuite

```bash
jinger run testcase.jinja.robot testdata.py testcase.robot
```

**Note**: For debugging purposes the variables that were replaced in the template can be printed as comments in the generated .robot file by passing the option `--debug` to `jinger run`.

## How it works

1. The .robot template file is converted to a Jinja template. This involves uncommenting the Jinja for-loop and replacing all RF variables of the form `${T_var}` with `{{var}}`.
2. Jinja processes the template.
3. The resulting list of testcases is written to the .robot file passed as last argument to `jinger run`
