import os
import argparse
import contextlib

with contextlib.suppress(ModuleNotFoundError):
    from crpack.__init__ import VERSION

    print(f"using crpack {VERSION}")


parser = argparse.ArgumentParser()
UNSPECIFIED = object()
parser.add_argument("-ver", "--version", nargs="?", choices=[None], default=UNSPECIFIED)
parser.add_argument("-n", "--name", nargs="?", default=None)
parser.add_argument("-d", "--desc", nargs="?", default=None)
parser.add_argument("-nf", "--new_folder", nargs="?", default=UNSPECIFIED)
args = parser.parse_args()
if args.version is None:
    print(f"Version of crpack is {VERSION}")
    quit(0)


def main():
    vstup = input("Name of package > ") if args.name is None else args.name
    desc = input("Description of package > ") if args.desc is None else args.desc
    nf = ""
    if args.new_folder is None:
        nf = input("Folder name for package to be put > ")
        nfpath = "" if nf in ["", "./"] else f"{nf}/"
    elif args.new_folder == UNSPECIFIED:
        nfpath = ".\\"
    else:
        nfpath = args.new_folder
    if args.new_folder != UNSPECIFIED:
        os.makedirs(f"{nf}/{vstup}")
    else:
        os.mkdir(vstup)
    with open(f"{nfpath}setup.py", "w") as file:
        file.write(
            f"""from setuptools import setup, find_packages
import glob
from {vstup} import VERSION, AUTHOR

setup(
    name="{vstup}",
    version=VERSION,
    description=\"{desc}"""
            + """\",
    author=AUTHOR,
    install_requires=[\"argparse\"],
    packages=find_packages(exclude=("tests*", "testing*")),
    include_package_data=True,
    package_data={"": glob.glob(__file__.rsplit(\"\\\\\", 1)[0] + \"\")},
    entry_points={
        "console_scripts": [
            \""""
            + vstup
            + """ = """
            + vstup
            + """."""
            + vstup
            + """:main\",
        ],
    },
)
"""
        )
    with open(f"{nfpath}{vstup}/__init__.py", "w") as file:
        file.write(
            """VERSION = \"1.0.0\"
AUTHOR = \"GrenManSK\"\n"""
        )
    with open(f"{nfpath}{vstup}/{vstup}.py", "w") as file:
        file.write(
            """import argparse
import sys
import contextlib

with contextlib.suppress(ModuleNotFoundError):
    from """
            + vstup
            + """.__init__ import VERSION

    print(f\"using """
            + vstup
            + """ {VERSION}")

explain = {}


def check_for_error(errors, func):
    \"\"\"Check for errors and print error messages.

    Args:
        errors: A dictionary or iterable of error codes.
        func: The function where the errors occurred.

    Returns:
        None

    \"\"\"
    
    if len(errors) == 0:
        return
    if isinstance(errors, dict):
        max_overflow = 15
        for error, data in errors.items():
            if len(data) > max_overflow:
                print(
                    f"ERROR: {func.__name__} failed with return code {error}; {data[:max_overflow]} ..."
                )
            else:
                print(f"ERROR: {func.__name__} failed with return code {error}; {data}")
    else:
        for error in errors:
            print(f"ERROR: {func.__name__} failed with return code {error}")

    print(f"\\nTry adding '--explain {min(errors)}' to see the error code")


def ErrorWrapper(func):
    \"\"\"Decorator that wraps a function and handles errors.

    Args:
        func: The function to be wrapped.

    Returns:
        The wrapped function.

    \"\"\"
    
    def wrapper(*args, **kwargs):
        try:
            return_code = func(*args, **kwargs)
            type_warnings = {
                str: "should not return a string but 0",
                bool: "should not return a bool but 0",
                float: "should not return a float but 0",
                bytes: "should not return a bytes but 0",
                bytearray: "should not return a bytearray but 0",
                list: check_for_error,
                tuple: check_for_error,
                set: check_for_error,
                dict: check_for_error,
            }
            if return_code == 0:
                sys.exit(0)
            elif return_code is None:
                print(f"WARNING: {func.__name__} should return 0")
            elif isinstance(return_code, tuple(type_warnings.keys())):
                warning = type_warnings[type(return_code)]
                if callable(warning):
                    warning(return_code, func)
                else:
                    print(f"WARNING: {func.__name__} {warning}")
            elif return_code == 1 and isinstance(return_code, int):
                print(f"ERROR: {func.__name__} failed with return code {return_code}")
            elif return_code != 0 and isinstance(return_code, int):
                print(
                    f"ERROR: {func.__name__} failed with return code {return_code}\\n\\nTry adding '--explain {return_code}' to see the error code"
                )
                sys.exit(return_code)
            else:
                print(
                    "WARNING: {} should return 0, not {}".format(
                        func.__name__, type(return_code)
                    )
                )
        except Exception as e:
            print(e)
            return 1

    return wrapper


@ErrorWrapper
def main():
    parser = argparse.ArgumentParser(
        prog=\""""
            + vstup
            + """\",
        description=\""""
            + desc
            + """\",
        epilog="",
    )
    err_group = parser.add_argument_group("EXPLAIN")
    err_group.add_argument(
        "--explain",
        type=lambda x: int(x) if x.isdigit() else str(x),
        help="explain error code",
        choices=list(explain.keys()) + ["all"],
        metavar="ERROR_CODE",
        dest="explain",
        default=None,
    )
    args = parser.parse_args()

    if args.explain is not None:
        if args.explain == "all":
            if len(explain) > 0:
                print("EXPLAIN: Explaining every error code:")
                for item in explain.keys():
                    print(f" EXPLAIN: {item}; {explain[item]}")
            else:
                print("EXPLAIN: Any error code supplied")
        else:
            print(f"EXPLAIN: Explaining error code: {args.explain}")
            print(f" EXPLAIN:  {explain[args.explain]}")
        return 0

    return 0


if __name__ == "__main__":
    main()
"""
        )


if __name__ == "__main__":
    main()
