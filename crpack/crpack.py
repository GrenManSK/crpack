import os
import argparse
import verbose
from crpack.__init__ import VERSION



logger = verbose.get_logger()
parser = argparse.ArgumentParser()
UNSPECIFIED = object()
parser.add_argument('-ver', '--version', nargs='?', default=UNSPECIFIED)
parser.add_argument('-v', '--verbose', nargs='?', default=UNSPECIFIED)
parser.add_argument('-n', '--name', nargs='?', default=None)
parser.add_argument('-d', '--desc', nargs='?', default=None)
parser.add_argument('-nf', '--new_folder', nargs='?', default=UNSPECIFIED)
args = parser.parse_args()
if args.version != None and args.version != UNSPECIFIED:
    print('Argument error: --version does not take any input')
    quit(1)
if args.version == None:
    print(f'Version of crpack is {VERSION}')
    quit(0)
if args.verbose == None:
    args.verbose = True
else:
    args.verbose = False


def main():
    nf = ''
    if args.name == None:
        vstup = input('Name of package > ')
    else:
        vstup = args.name
    if args.desc == None:
        desc = input('Description of package > ')
    else:
        desc = args.desc
    if args.new_folder in [None, UNSPECIFIED]:
        nf = input('Folder name for package to be put > ')
        if nf in ['', './']:
            nfpath = ''
        else:
            nfpath = nf + '/'
    else:
        nf = args.new_folder
        nfpath = nf + '/'


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
    with open(f'{nfpath}setup.py', 'w') as file:
        file.write(f"""from setuptools import setup
from setuptools import find_packages
from {vstup} import VERSION, AUTHOR

setup(
    name ='{vstup}' ,
    version=VERSION,
    description='""" + desc + """',
    author=AUTHOR,
    install_requires=[],
    packages=find_packages(exclude=('tests*', 'testing*')),
    entry_points={
        'console_scripts': [
            '""" + vstup + """ = """ + vstup + """.""" + vstup + """:main',
],
}
)
""")
    if args.verbose:
        logger.stay(f"Writing __init__.py")
    with open(f"{nfpath}{vstup}/__init__.py", 'w') as file:
        file.write("""VERSION = '1.0.0'
AUTHOR = 'GrenManSK'""")
    if args.verbose:
        logger.stay(f"Writing {vstup}.py")
    with open(f"{nfpath}{vstup}/{vstup}.py", 'w') as file:
        file.write("""def main():
    pass


if __name__ == '__main__':
    main()""")


if __name__ == '__main__':
    main()
