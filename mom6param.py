#!/usr/bin/env python

from __future__ import print_function

import re

# TODO: Replace "token: token" with actual tokens, e.g.
#   lambda scanner, token: ("String", token)
# TODO: Leading digit could be .01, but we assume it starts with 0-9!
# TODO: Preserve whitespace and comments
param_scanner = re.Scanner([
    # Identifiers
    (r'[A-Za-z][_0-9a-zA-z]*', lambda scanner, token: token),
    # Number literals
    (r'-?[0-9][0-9]*\.?[0-9]*([eE]?[+-]?[0-9][0-9]*)?', lambda scanner, token: token),
    # String literals
    # NOTE: Does MOM6 param use Fortran escape delimiters?
    (r'"[^"]*"("[^"]*")*', lambda scanner, token: token),
    (r"'[^']*'('[^']*')*", lambda scanner, token: token),
    # Operators
    (r'=', lambda scanner, token: token),
    (r'%', lambda scanner, token: token),
    (r',', lambda scanner, token: token),
    (r'\*', lambda scanner, token: token),
    # Preprocessing (TODO)
    #(r'\#override', lambda scanner, token: token),
    (r'#.*', None),
    # Comments
    (r'!.*', None),
    # Whitespace
    (r'\s+', None),
])

def parse_file(file):
    params = {}

    for line in param_file:
        # Tokenize line
        tokens, remainder = param_scanner.scan(line)

        # Validate tokenization
        if remainder:
            print('Untokenized characters:')
            print('Line:', repr(line))
            print('Tokens:', tokens)
            print('Unscanned:', remainder)
            raise

        # NOTE: Just a dumb hand parser.  Rewrite as a proper grammar.

        # Skip blank lines
        if tokens == []:
            continue

        tok = tokens[0]

        # Terminating parameter block?
        if tok == '%':
            block = tokens[1]
            # TODO: Assert block name?
            return params

        if tokens[1] == '%':
            params[tok] = parse_file(file)
            continue

        # Else..
        assert tokens[1] == '='

        # TODO: Convert value based on token type

        if ',' in tokens[2:]:
            value = [v for v in tokens[2:] if v != ',']
        elif '*' in tokens[2:]:
            assert len(tokens) == 5
            assert tokens[3] == '*'

            nvals = int(tokens[2])
            value = nvals * [tokens[4]]
        else:
            if len(tokens) != 3:
                print ('oh no!')
                print(tokens)
                raise

            value = tokens[2]

        params[tok] = value

    return params

# Main...

param_file = open('MOM_parameter_doc.all')
param_data = parse_file(param_file)
param_file.close()
