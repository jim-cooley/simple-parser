from argparse import ArgumentParser

from parser.lexer import Lexer
from runtime.exceptions import getLogFacility
from runtime.options import getOptions
from runtime.runtime import load_script

LOG_FILE = './lexer.log'

_option_defaults = {
    'file': None,           # auto run a script file
    'verbose': True,
}


class LexConsole:
    def __init__(self, options=None, file=None):
        self.logger = getLogFacility('lexer', lines=None, file=file)
        self.option = getOptions('lexer', options=vars(options), defaults=_option_defaults)
        pass

    def load(self, fname):
        if self.option.verbose:
            print(f'\n\nloading {fname}...')
        source = load_script(fname)
        return source

    def go(self, ):
        fname = self.option.file
        source = self.load(fname)
        lexer = Lexer(source=source, verbose=self.option.verbose)
        print('source:')
        print(source)
        print('tokens:')
        lexer.printall()


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-f', '--file', default=None, help="script file to execute")
    parser.add_argument('file', nargs='?', default=None, help="script file to execute")
    parser.add_argument('-q', '--quiet', dest='verbose', action='store_false', help="less verbose output")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="more verbose output")
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    with open(LOG_FILE, 'w') as log:
        lexer = LexConsole(args, file=log)
        lexer.go()
