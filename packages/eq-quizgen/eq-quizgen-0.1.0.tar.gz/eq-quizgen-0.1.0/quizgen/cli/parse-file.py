import argparse
import sys

import quizgen.constants
import quizgen.parser

def run(args):
    document = quizgen.parser.parse_file(args.path)

    content = document.to_format(args.format, full_doc = args.full_doc)
    print(content)

    return 0

def _get_parser():
    parser = argparse.ArgumentParser(description =
        "Parse a single file and output the results of the parse.")

    parser.add_argument('path',
        type = str,
        help = 'The path to parse.')

    parser.add_argument('--format',
        action = 'store', type = str, default = quizgen.constants.DOC_FORMAT_JSON,
        choices = quizgen.constants.DOC_FORMATS,
        help = 'Output the parsed document in this format (default: %(default)s).')

    parser.add_argument('--full', dest = 'full_doc',
        action = 'store_true', default = False,
        help = 'Treat the output as a fill document instead of just a snippet, e.g. TeX will output a full document (default: %(default)s)')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
