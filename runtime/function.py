from dataclasses import dataclass

from runtime.environment import Environment
from runtime.scope import Scope, FunctionBase


@dataclass
class Function(FunctionBase):
    def __init__(self, name=None, members=None, arity=None, opt=None, defaults=None, parameters=None, other=None, tid=None, loc=None, is_lvalue=True):
        super().__init__(name=name, other=other, members=members, arity=arity, opt=opt, parameters=parameters, defaults=defaults, tid=tid, loc=loc, is_lvalue=is_lvalue)

    def __len__(self):
        return len(self._members)

    def count(self):
        """
        Parameter count.  Defines the Function's signature
        """
        return len(self.defaults)

    def invoke(self, interpreter, args=None):
        scope = Scope(other=self)
        scope.update_members(args)
        Environment.enter(scope)
        interpreter.visit(self.code)
        Environment.leave()
        return interpreter.stack.pop()
