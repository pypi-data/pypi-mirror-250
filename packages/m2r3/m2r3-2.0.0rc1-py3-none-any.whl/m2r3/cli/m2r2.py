import os
from argparse import ArgumentParser, Namespace

from ..m2r2 import convert

parser = ArgumentParser()
options = Namespace()
parser.add_argument("input_file", nargs="*", help="files to convert to reST format")
parser.add_argument(
    "--overwrite",
    action="store_true",
    default=False,
    help="overwrite output file without confirmaion",
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    default=False,
    help="print conversion result and not save output file",
)
parser.add_argument(
    "--no-underscore-emphasis",
    action="store_true",
    default=False,
    help="do not use underscore (_) for emphasis",
)
parser.add_argument(
    "--parse-relative-links",
    action="store_true",
    default=False,
    help="parse relative links into ref or doc directives",
)
parser.add_argument(
    "--anonymous-references",
    action="store_true",
    default=False,
    help="use anonymous references in generated rst",
)
parser.add_argument(
    "--disable-inline-math",
    action="store_true",
    default=False,
    help="disable parsing inline math",
)


def parse_options():
    parser.parse_known_args(namespace=options)


def parse_from_file(file, encoding="utf-8", **kwargs):
    if not os.path.exists(file):
        raise OSError("No such file exists: {}".format(file))
    with open(file, encoding=encoding) as f:
        src = f.read()
    output = convert(src, **kwargs)
    return output


def save_to_file(file, src, encoding="utf-8", **kwargs):
    target = os.path.splitext(file)[0] + ".rst"
    if not options.overwrite and os.path.exists(target):
        confirm = input("{} already exists. overwrite it? [y/n]: ".format(target))
        if confirm.upper() not in ("Y", "YES"):
            print("skip {}".format(file))
            return
    with open(target, "w", encoding=encoding) as f:
        f.write(src)


def main():
    parse_options()  # parse cli options
    if not options.input_file:
        parser.print_help()
        parser.exit(0)
    for file in options.input_file:
        output = parse_from_file(file)
        if options.dry_run:
            print(output)
        else:
            save_to_file(file, output)


if __name__ == "__main__":
    main()
