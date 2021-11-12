# Python-based Parser
#
from parser.lexer import Lexer


def main():
    scanner = Lexer(source="buy = { close >> sma(10) and close >> sma(20) } @ open.delay(1d)")


if __name__ == '__main__':
    main()
