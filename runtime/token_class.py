from enum import unique, IntEnum, auto


@unique
class TCL(IntEnum):
    NONE = 0
    BINOP = auto()
    DATASET = auto()  # dataset, panda
    FUNCTION = auto()
    KEYWORD = auto()
    LITERAL = auto()
    IDENTIFIER = auto()
    SCOPE = auto()
    TUPLE = auto()
    UNARY = auto()
    ERROR = auto()
