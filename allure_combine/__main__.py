import argparse

from allure_combine.combine import DEFAULT_HTML, combine_allure


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('folder', help='Path to allure report directory')
    parser.add_argument('--dest', default=None,
                        help='Path where the single html file will be stored. '
                             f'If argument does not end with .html, {DEFAULT_HTML} is appended.'
                             f'If omitted, output is written to {DEFAULT_HTML} in allure report directory')
    parser.add_argument("--auto-create-folders", action="store_true",
                        help="Whether auto create dest folders or not when folder does not exist. Default is false.")
    parser.add_argument("--ignore-utf8-errors", action="store_true",
                        help="If test files does contain some broken unicode, decode errors would be ignored")
    args = parser.parse_args()

    combine_allure(args.folder, args.dest, args.auto_create_folders, args.ignore_utf8_errors)


if __name__ == '__main__':
    main()
