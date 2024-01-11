# Custom exception and warning formatter [![PyPI](https://img.shields.io/pypi/v/mwk-traceback)](https://pypi.org/project/mwk-traceback/) 

---

## Exceptions
### Define exception format by subclassing **CustomTraceback**
```python
class MyTracebackFormatter(CustomTraceback):
    _EXC_FORMAT = '| {traceback}>> {type}: {exception}.\n'
    _TB_FORMAT = '[{file}::{func}]@{line} "{code}" | '
    _EXC_HOOK_HEAD_TEXT = 'Error:'
```
*1. **_EXC_FORMAT** used for formatting single exception in exceptions chain:*  
**_EXC_FORMAT** should be *python formatted string literal* with values in **{}** brackets.
Available values for **_EXC_FORMAT** *formatted string literal*:
- **traceback**: formatted traceback goes here (see below)
- **type**: exception class name
- **exception**: exception message  

*2. **_TB_FORMAT** used for formatting single traceback frame in traceback chain:*  
**_TB_FORMAT** should be *python formatted string literal* with values in **{}** brackets.
Available values for **_TB_FORMAT** *formatted string literal*:
- **file**: python .py file stem where error occurred
- **func**: function or module where error occurred
- **line**: number of the line of code where error occurred  
- **code**: line of code itself

*3. **_EXC_HOOK_HEAD_TEXT** used as header for exceptions*  
**_EXC_HOOK_HEAD_TEXT** should be python string

*4. Additional variables to define:*
- **_EXC_OUT**: output for exceptions, **sys.stderr**  by default
- **_EXC_CHAIN**: **True** - chain exceptions, **False** - only last exception, by default **True**
- **_EXC_REVERSE**: order of chained exceptions, **True** - show like default python exception hook, by default **False**
### Usage:
1. Definition
```python
class MyTracebackFormatter(CustomTraceback):
    _TB_FORMAT = '[{file}::{func}]@{line} "{code}" | '
    _EXC_FORMAT = '| {traceback}>> {type}: {exception}.\n'
    _EXC_HOOK_HEAD_TEXT = 'Error:'
    _EXC_OUT = sys.stderr
    _EXC_CHAIN = True
    _EXC_REVERSE = False
```
2. Get formatted exception string
```python
exc_str = MyTracebackFormatter(exc)
```
3. Print formatted exception
```python
MyTracebackFormatter.print_exception(exc)
```
4. Use with **sys.excepthook**
```python
import sys
sys.excepthook = MyTracebackFormatter.exception_hook
```
### Predefined traceback formatters
1. **compact_tb**
```python
from mwk_traceback import compact_tb
import sys
sys.excepthook = compact_tb.exception_hook

main()  # ! check test dir for code !
```
Output:
```commandline
Error(s):
| Error in [test_exc_tb.py] in [<module>] at line (39) while executing "main()"
| Error in [test_exc_tb.py] in [main] at line (27) while executing "func()"
| Error in [test_exc_tb.py] in [func] at line (22) while executing "raise"
   >> NameError: error in func.
| Error in [test_exc_tb.py] in [func] at line (20) while executing "func_func()"
| Error in [test_exc_tb.py] in [func_func] at line (15) while executing "raise"
   >> AttributeError: error in func_func.
| Error in [test_exc_tb.py] in [func_func] at line (13) while executing "func_func_func()"
| Error in [test_exc_tb.py] in [func_func_func] at line (8) while executing "x = 1 / 0"
   >> ZeroDivisionError: division by zero.
```
2. **super_compact_tb**
```python
from mwk_traceback import super_compact_tb
import sys
sys.excepthook = super_compact_tb.exception_hook

main()  # ! check test dir for code !
```
Output:
```commandline
Error:
| [test_exc_tb::<module>]@42 "main()" | [test_exc_tb::main]@27 "func()" | [test_exc_tb::func]@22 "raise" | >> NameError: error in func.
| [test_exc_tb::func]@20 "func_func()" | [test_exc_tb::func_func]@15 "raise" | >> AttributeError: error in func_func.
| [test_exc_tb::func_func]@13 "func_func_func()" | [test_exc_tb::func_func_func]@8 "x = 1 / 0" | >> ZeroDivisionError: division by zero.
```
## Warnings
### Define warning format by subclassing **CustomWarningFormatter**:
```python
class MyWarningFormatter(CustomWarningFormatter):
    _WARN_FORMAT = '[{file}]@{line} >> {type}: {message}\n'
```
**_WARN_FORMAT** should be *python formatted string literal* with values in **{}** brackets.  
Available values for **_WARN_FORMAT** *formatted string literal*:
- **message**: warning message
- **type**: warning class name
- **file**: python .py file stem where warning occurred
- **line**: number of the line of code where warning occurred
### Usage:
```python
import warnings
warnings.formatwarning = MyWarningFormatter

warnings.warn('This is warning', UserWarning)
```
### Predefined warning formatters (classes)
1. **compact_warn**
```python
import warnings
from mwk_traceback import compact_warn
warnings.formatwarning = compact_warn

warnings.warn('This is warning', DeprecationWarning)
```
Output:
```commandline
Warning in [test_warn.py] at line (6)
   >> DeprecationWarning: This is warning
```
2. **super_compact_warn**
```python
import warnings
from mwk_traceback import super_compact_warn
warnings.formatwarning = super_compact_warn

warnings.warn('This is another warning', UserWarning)
```
Output:
```commandline
[test_warn]@10 >> UserWarning: This is another warning
```

