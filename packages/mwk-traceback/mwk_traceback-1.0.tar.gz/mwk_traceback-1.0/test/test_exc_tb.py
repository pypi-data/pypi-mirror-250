import sys

from mwk_traceback import compact_tb as c_tb
from mwk_traceback import super_compact_tb as sc_tb


def func_func_func():
    x = 1 / 0


def func_func():
    try:
        func_func_func()
    except Exception as exc:
        raise AttributeError('error in func_func') from exc


def func():
    try:
        func_func()
    except Exception as exc:
        raise NameError('error in func') from exc


def main():

    func()


if __name__ == '__main__':
    test_prints = (c_tb, sc_tb)
    for t in test_prints:
        try:
            main()
        except Exception as exc:
            t.print_exception(exc)

    # sys.excepthook = c_tb.exception_hook
    # main()

    sys.excepthook = sc_tb.exception_hook
    main()
