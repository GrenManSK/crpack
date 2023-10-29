import os
import argparse
import verbose
from crpack.__init__ import VERSION


logger = verbose.get_logger()
parser = argparse.ArgumentParser()
UNSPECIFIED = object()
parser.add_argument("-ver", "--version", nargs="?", default=UNSPECIFIED)
parser.add_argument("-v", "--verbose", nargs="?", default=UNSPECIFIED)
parser.add_argument("-n", "--name", nargs="?", default=None)
parser.add_argument("-d", "--desc", nargs="?", default=None)
parser.add_argument("-nf", "--new_folder", nargs="?", default=UNSPECIFIED)
args = parser.parse_args()
if args.version != None and args.version != UNSPECIFIED:
    print("Argument error: --version does not take any input")
    quit(1)
if args.version == None:
    print(f"Version of crpack is {VERSION}")
    quit(0)
if args.verbose == None:
    args.verbose = True
else:
    args.verbose = False


def main():
    nf = ""
    if args.name == None:
        vstup = input("Name of package > ")
    else:
        vstup = args.name
    if args.desc == None:
        desc = input("Description of package > ")
    else:
        desc = args.desc
    if args.new_folder is None:
        nf = input("Folder name for package to be put > ")
        if nf in ["", "./"]:
            nfpath = ""
        else:
            nfpath = nf + "/"
    else:
        nfpath = args.new_folder

    if args.verbose:
        logger.stay(f"Creating folder with name {vstup}")
    if args.new_folder != UNSPECIFIED:
        if args.verbose:
            logger.stay(f"Creating folder with name {nf}")
            logger.stay(f"Creating folder with name {nf}/{vstup}")
        os.mkdir(f"{nf}")
        os.mkdir(f"{nf}/{vstup}")
    else:
        if args.verbose:
            logger.stay(f"Creating folder with name {vstup}")
        os.mkdir(f"{vstup}")
    if args.verbose:
        logger.stay(f"Writing setup.py")
    with open(f"{nfpath}setup.py", "w") as file:
        file.write(
            f"""from setuptools import setup
from setuptools import find_packages
import glob
from {vstup} import VERSION, AUTHOR

setup(
    name="{vstup}",
    version=VERSION,
    description=\""""
            + desc
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
    if args.verbose:
        logger.stay(f"Writing __init__.py")
    with open(f"{nfpath}{vstup}/__init__.py", "w") as file:
        file.write(
            """VERSION = '1.0.0'
AUTHOR = 'GrenManSK'"""
        )
    if args.verbose:
        logger.stay(f"Writing {vstup}.py")
    with open(f"{nfpath}{vstup}/{vstup}.py", "w") as file:
        file.write(
            """import argparse
import sys

explain = {}


def check_for_error(errors, func):
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

    print(f"\nTry adding '--explain {min(errors)}' to see the error code")


def ErrorWrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return_code = func(*args, **kwargs)
            if return_code == 0:
                sys.exit(0)
            elif return_code is None:
                print(f"WARNING: {func.__name__} should return 0")
            elif isinstance(return_code, str):
                print(f"WARNING: {func.__name__} should not return a string but 0")
            elif isinstance(return_code, bool):
                print(f"WARNING: {func.__name__} should not return a bool but 0")
            elif isinstance(return_code, float):
                print(f"WARNING: {func.__name__} should not return a float but 0")
            elif isinstance(return_code, (list, tuple, set, dict)):
                check_for_error(return_code, func)
            elif isinstance(return_code, bytes):
                print(f"WARNING: {func.__name__} should not return a bytes but 0")
            elif isinstance(return_code, bytearray):
                print(f"WARNING: {func.__name__} should not return a bytearray but 0")
            elif return_code == 1 and isinstance(return_code, int):
                print(f"ERROR: {func.__name__} failed with return code {return_code}")
            elif return_code != 0 and isinstance(return_code, int):
                print(
                    f"ERROR: {func.__name__} failed with return code {return_code}\n\nTry adding '--explain {return_code}' to see the error code"
                )
                sys.exit(return_code)
            else:
                print(
                    "WARNING: "
                    + func.__name__
                    + f" should return 0, not {type(return_code)}"
                )
        except Exception as e:
            print(e)
            return 1

    return wrapper


@ErrorWrapper
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--explain",
        type=int,
        help="explain error code",
        choices=explain.keys(),
        metavar="ERROR_CODE",
        default=None,
    )
    args = parser.parse_args()

    if args.explain is not None:
        print(f"EXPLAIN: Explaining error code: {args.explain}")
        print(" EXPLAIN:  " + explain[args.explain])
        return 0

    return 0


if __name__ == "__main__":
    main()
"""
        )


if __name__ == "__main__":
    main()
