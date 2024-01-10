# __main__.py

import argparse

from .get_alpha3 import get_alpha3_code


def main():
    parser = argparse.ArgumentParser(description='The tools helps to find Alpha3 code for a input country name')

    # Add positional argument to the parser.
    parser.add_argument("country", type=str, help="Name of country")

    # Parse the command-line arguments provided by the user.
    args = parser.parse_args()

    # Make API call 
    alpha3code = get_alpha3_code(args.country)
    
    if alpha3code:
        print(alpha3code)


if __name__ == '__main__':  # pragma: no cover
    main()
