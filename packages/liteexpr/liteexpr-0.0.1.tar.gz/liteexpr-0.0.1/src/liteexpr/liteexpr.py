__copyright__ = "Copyright 2023-2024 Mark Kim"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__author__ = "Mark Kim"

import math
import antlr4
from .LiteExprLexer import LiteExprLexer
from .LiteExprParser import LiteExprParser
from .LiteExprVisitor import LiteExprVisitor


##############################################################################
# CONSTANTS

INTMASK = 0xffffffffffffffff


##############################################################################
# PUBLIC FUNCTIONS

def evalfd(fd, symbols=None):
    code = fd.read()

    return eval(code, symbols)


def eval(code, symbols=None):
    compiled = compile(str(code))

    return compiled.eval(symbols)


def compile(code):
    try:
        lexer = LiteExprLexer(antlr4.InputStream(code))
        parser = LiteExprParser(antlr4.CommonTokenStream(lexer))
        parser._errHandler = antlr4.error.ErrorStrategy.BailErrorStrategy()
        tree = parser.file_()
    except antlr4.error.Errors.ParseCancellationException as e:
        t = e.args[0].offendingToken

        raise LE_SyntaxError(f"Unexpected token `{t.text}`", t.line, t.column) from None

    return LE_Compiled(tree)


def compilefd(fd):
    code = fd.read()

    return compile(code)


##############################################################################
# EXCEPTIONS

class LE_Error(Exception):
    def __init__(self, text, line=None, column=None):
        if   column is None and line is None : super().__init__(f"{text}")
        elif column is None                  : super().__init__(f"[line {line}] {text}")
        else                                 : super().__init__(f"[line {line}, col {column}] {text}")

class LE_SyntaxError(LE_Error): pass
class LE_RuntimeError(LE_Error): pass


##############################################################################
# HELPER CLASSES

class LE_Compiled:
    def __init__(self, tree):
        self.tree = tree

    def eval(self, symbolTable=None):
        evaluator = LE_Evaluator(symbolTable)
        evaluator.visit(self.tree)

        return evaluator.result[self.tree]


class LE_SymbolTable:
    def __init__(self, symbols=dict(), parent=None):
        self.symbols = builtins | symbols if parent is None else symbols
        self.parent = parent

    def __getitem__(self, name):
        name = str(name)

        if name in self.symbols : return self.symbols[name]
        else                    : return self.parent[name]

    def __setitem__(self, name, value):
        name = str(name)

        self.symbols[name] = value

        return self.symbols[name]

    def __str__(self):
        import json

        return json.dumps(self.symbols, indent=2, default=str)


##############################################################################
# TYPES

class LE_Variable:
    def __init__(self, name, container):
        self.name = name
        self.container = container

    @property
    def value(self):
        if   isinstance(self.container, LE_SymbolTable) : return self.container[self.name]
        elif isinstance(self.container, list)           : return self.container[self.name]
        elif isinstance(self.container, dict)           : return self.container[self.name]
        else                                            : return self.container

    @value.setter
    def value(self, value):
        if   isinstance(self.container, LE_SymbolTable) : self.container[self.name] = value
        elif isinstance(self.container, list)           : self.container[self.name] = value
        elif isinstance(self.container, dict)           : self.container[self.name] = value
        else                                            : self.container = value

        return value


class LE_Int(int):
    @property
    def value(self):
        return self


class LE_Double(float):
    @property
    def value(self):
        return self


class LE_String(str):
    @property
    def value(self):
        return self


class LE_Array(list):
    @property
    def value(self):
        return self


class LE_Object(dict):
    @property
    def value(self):
        return self


##############################################################################
# EVALUATOR

class LE_Evaluator(LiteExprVisitor):
    def __init__(self, symbolTable=None):
        super().__init__()
        self.result = dict()
        self.symbolTable = LE_SymbolTable() if symbolTable is None else symbolTable

    def visitFile(self, ctx):
        self.visitChildren(ctx)

        lastExpr = ctx.expr()[-1]

        self.result[ctx] = self.result[lastExpr].value

        return self.result[ctx]

    def visitString(self, ctx):
        if ctx not in self.result:
            try:
                self.result[ctx] = LE_String(_decodeString(ctx.STRING().getText()[1:-1]))
            except LE_SyntaxError as e:
                raise LE_SyntaxError(str(e), ctx.start.line, ctx.start.column) from None

        return self.result[ctx]

    def visitDouble(self, ctx):
        if ctx not in self.result:
            self.result[ctx] = LE_Double(ctx.DOUBLE().getText())

        return self.result[ctx]

    def visitHex(self, ctx):
        if ctx not in self.result:
            self.result[ctx] = LE_Int(ctx.HEX().getText()[2:], 16)

        return self.result[ctx]

    def visitInt(self, ctx):
        if ctx not in self.result:
            self.result[ctx] = LE_Int(ctx.INT().getText())

        return self.result[ctx]

    def visitCall(self, ctx):
        self.visit(ctx.varname())
        fn = self.result[ctx.varname()].value

        if hasattr(fn, "opts") and fn.opts["delayvisit"]:
            args = ctx.list_().expr()
        else:
            self.visit(ctx.list_())
            args = self.result[ctx.list_()].value

        try:
            self.result[ctx] = fn(*args, visitor=self, sym=self.symbolTable)
        except LE_SyntaxError as e:
            raise LE_SyntaxError(f"Syntax error while executing {ctx.getText()}: {str(e)}", ctx.start.line, ctx.start.column) from None
        except LE_RuntimeError as e:
            raise LE_RuntimeError(f"Runtime error while executing {ctx.getText()}: {str(e)}", ctx.start.line, ctx.start.column) from None

        return self.result[ctx]

    def visitVariable(self, ctx):
        self.visitChildren(ctx)

        self.result[ctx] = self.result[ctx.varname()]

        return self.result[ctx]

    def visitObject(self, ctx):
        self.visitChildren(ctx)

        self.result[ctx] = self.result[ctx.pairlist()]

        return self.result[ctx]

    def visitArray(self, ctx):
        self.visitChildren(ctx)

        self.result[ctx] = self.result[ctx.list_()]

        return self.result[ctx]

    def visitParen(self, ctx):
        self.visitChildren(ctx)

        self.result[ctx] = self.result[ctx.expr()]

        return self.result[ctx]

    def visitPostfixOp(self, ctx):
        self.visitChildren(ctx)

        var = self.result[ctx.varname()]
        op = ctx.op.text
        T = type(var.value)

        if   op == "++" : self.result[ctx] = var.value; var.value = T(var.value + 1)
        elif op == "--" : self.result[ctx] = var.value; var.value = T(var.value - 1)
        else            : raise LE_SyntaxError("Unknown postfix operator `{op}`", ctx.start.line, ctx.start.column)

        return self.result[ctx]

    def visitPrefixOp(self, ctx):
        self.visitChildren(ctx)

        var = self.result[ctx.varname()]
        op = ctx.op.text
        T = type(var.value)

        if   op == "++" : var = T(var.value + 1); self.result[ctx] = var.value
        elif op == "--" : var = T(var.value - 1); self.result[ctx] = var.value
        else            : raise LE_SyntaxError("Unknown prefix operator `{op}`", ctx.start.line, ctx.start.column)

        return self.result[ctx]

    def visitUnaryOp(self, ctx):
        self.visitChildren(ctx)

        value = self.result[ctx.expr()].value
        op = ctx.op.text
        T = type(value)

        if   op == "!"  : self.result[ctx] = LE_Int(not value)
        elif op == "~"  : self.result[ctx] = LE_Int(~value)
        elif op == "+"  : self.result[ctx] = value
        elif op == "-"  : self.result[ctx] = T(-value)
        else            : raise LE_SyntaxError("Unknown unary operator `{op}`", ctx.start.line, ctx.start.column)

        return self.result[ctx]

    def visitBinaryOp(self, ctx):
        op = ctx.op.text

        if   op == "**"  : self.result[ctx] = _op_pow(*ctx.expr(), visitor=self)
        elif op == "*"   : self.result[ctx] = _op_mul(*ctx.expr(), visitor=self)
        elif op == "/"   : self.result[ctx] = _op_div(*ctx.expr(), visitor=self)
        elif op == "+"   : self.result[ctx] = _op_add(*ctx.expr(), visitor=self)
        elif op == "-"   : self.result[ctx] = _op_sub(*ctx.expr(), visitor=self)
        elif op == "%"   : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value %   self.visit(ctx.expr(1)).value)
        elif op == "<<"  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value <<  self.visit(ctx.expr(1)).value)
        elif op == ">>"  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value >>  self.visit(ctx.expr(1)).value)
        elif op == "<"   : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value <   self.visit(ctx.expr(1)).value)
        elif op == "<="  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value <=  self.visit(ctx.expr(1)).value)
        elif op == ">"   : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value >   self.visit(ctx.expr(1)).value)
        elif op == ">="  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value >=  self.visit(ctx.expr(1)).value)
        elif op == "=="  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value ==  self.visit(ctx.expr(1)).value)
        elif op == "!="  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value !=  self.visit(ctx.expr(1)).value)
        elif op == "&"   : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value &   self.visit(ctx.expr(1)).value)
        elif op == "^"   : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value ^   self.visit(ctx.expr(1)).value)
        elif op == "|"   : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value |   self.visit(ctx.expr(1)).value)
        elif op == "&&"  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value and self.visit(ctx.expr(1)).value)
        elif op == "||"  : self.result[ctx] = LE_Int(self.visit(ctx.expr(0)).value or  self.visit(ctx.expr(1)).value)
        elif op == ">>>" : self.result[ctx] = LE_Int((self.visit(ctx.expr(0)).value & INTMASK) >> self.visit(ctx.expr(1)).value)
        else             : raise LE_SyntaxError("Unknown binary operator `{op}`", ctx.start.line, ctx.start.column)

        return self.result[ctx]

    def visitAssignOp(self, ctx):
        op = ctx.op.text
        var = self.visit(ctx.varname())

        if   op == "="    : self.result[ctx] = self.visit(ctx.expr()).value
        elif op == "**="  : self.result[ctx] = _op_pow(var, ctx.expr(), visitor=self)
        elif op == "*="   : self.result[ctx] = _op_mul(var, ctx.expr(), visitor=self)
        elif op == "/="   : self.result[ctx] = _op_div(var, ctx.expr(), visitor=self)
        elif op == "+="   : self.result[ctx] = _op_add(var, ctx.expr(), visitor=self)
        elif op == "-="   : self.result[ctx] = _op_sub(var, ctx.expr(), visitor=self)
        elif op == "%="   : self.result[ctx] = LE_Int(var.value %   self.visit(ctx.expr()).value)
        elif op == "<<="  : self.result[ctx] = LE_Int(var.value <<  self.visit(ctx.expr()).value)
        elif op == ">>="  : self.result[ctx] = LE_Int(var.value >>  self.visit(ctx.expr()).value)
        elif op == "&="   : self.result[ctx] = LE_Int(var.value &   self.visit(ctx.expr()).value)
        elif op == "^="   : self.result[ctx] = LE_Int(var.value ^   self.visit(ctx.expr()).value)
        elif op == "|="   : self.result[ctx] = LE_Int(var.value |   self.visit(ctx.expr()).value)
        elif op == "&&="  : self.result[ctx] = LE_Int(var.value and self.visit(ctx.expr()).value)
        elif op == "||="  : self.result[ctx] = LE_Int(var.value or  self.visit(ctx.expr()).value)
        elif op == ">>>=" : self.result[ctx] = LE_Int((var.value & INTMASK) >> self.visit(ctx.expr()).value)
        else              : raise LE_SyntaxError("Unknown assign operator `{op}`", ctx.start.line, ctx.start.column)

        var.value = self.result[ctx]

        return self.result[ctx]

    def visitTertiaryOp(self, ctx):
        op = (
            ctx.op1.text,
            ctx.op2.text,
        )

        if op[0] == "?" and op[1] == ":" : self.result[ctx] = self.visit(ctx.expr(1)).value if self.visit(ctx.expr(0)).value else self.visit(ctx.expr(2)).value
        else                             : raise LE_SyntaxError("Unknown tertiary operator `{op[0]} {op[1]}`", ctx.start.line, ctx.start.column)

        return self.result[ctx]

    def visitIndexedVar(self, ctx):
        self.visitChildren(ctx)

        array = self.result[ctx.varname()].value
        index = self.result[ctx.expr()].value

        self.result[ctx] = LE_Variable(index, array)

        return self.result[ctx]

    def visitMemberVar(self, ctx):
        self.visitChildren(ctx)

        base = self.result[ctx.varname(0)].value
        member = self.result[ctx.varname(1)].name

        self.result[ctx] = LE_Variable(member, base)

        return self.result[ctx]

    def visitSimpleVar(self, ctx):
        self.visitChildren(ctx)

        varname = ctx.ID().getText()

        self.result[ctx] = LE_Variable(varname, self.symbolTable)

        return self.result[ctx]

    def visitPairlist(self, ctx):
        self.visitChildren(ctx)

        self.result[ctx] = LE_Object()

        for pair in ctx.pair():
            for k,v in self.result[pair].items():
                self.result[ctx][k] = v

        return self.result[ctx]

    def visitPair(self, ctx):
        self.visitChildren(ctx)

        name = ctx.ID().getText()
        value = self.result[ctx.expr()]

        self.result[ctx] = { LE_String(name) : value }

        return self.result[ctx]

    def visitList(self, ctx):
        self.visitChildren(ctx)

        self.result[ctx] = LE_Array()

        for item in ctx.expr():
            self.result[ctx] += [self.result[item].value]

        return self.result[ctx]


def _op_pow(*args, **kwargs):
    visitor = kwargs["visitor"]
    value = (
        args[0].value if isinstance(args[0],LE_Variable) else visitor.visit(args[0]).value,
        visitor.visit(args[1]).value,
    )
    T = LE_Int if isinstance(value[0],int) and isinstance(value[1],int) else LE_Double

    return (LE_Double if value[1] < 0 else T)(value[0] ** value[1])


def _op_mul(*args, **kwargs):
    visitor = kwargs["visitor"]
    value = (
        args[0].value if isinstance(args[0],LE_Variable) else visitor.visit(args[0]).value,
        visitor.visit(args[1]).value,
    )
    T = LE_Int if isinstance(value[0],int) and isinstance(value[1],int) else LE_Double

    return T(value[0] * value[1])


def _op_div(*args, **kwargs):
    visitor = kwargs["visitor"]
    value = (
        args[0].value if isinstance(args[0],LE_Variable) else visitor.visit(args[0]).value,
        visitor.visit(args[1]).value,
    )
    T = LE_Int if isinstance(value[0],int) and isinstance(value[1],int) else LE_Double

    return T(value[0] / value[1])


def _op_add(*args, **kwargs):
    visitor = kwargs["visitor"]
    value = (
        args[0].value if isinstance(args[0],LE_Variable) else visitor.visit(args[0]).value,
        visitor.visit(args[1]).value,
    )
    T = LE_Int if isinstance(value[0],int) and isinstance(value[1],int) else LE_Double

    return LE_String(str(value[0]) + str(value[1])) if isinstance(value[0],str) or isinstance(value[1],str) else T(value[0] + value[1])


def _op_sub(*args, **kwargs):
    visitor = kwargs["visitor"]
    value = (
        args[0].value if isinstance(args[0],LE_Variable) else visitor.visit(args[0]).value,
        visitor.visit(args[1]).value,
    )
    T = LE_Int if isinstance(value[0],int) and isinstance(value[1],int) else LE_Double

    return T(value[0] - value[1])


##############################################################################
# HELPER FUNCTIONS

def _decodeString(s):
    decoded = ""
    i = 0

    while i < len(s):
        if   s[i:i+2] == "\\\\"   : decoded += "\\"; i+=2
        elif s[i:i+2] == "\\\""   : decoded += "\""; i+=2
        elif s[i:i+3] == "\\\r\n" : i+=2
        elif s[i:i+2] == "\\\r"   : i+=2
        elif s[i:i+2] == "\\\n"   : i+=2
        elif s[i:i+2] == "\\t"    : decoded += "\t"; i+=2
        elif s[i:i+2] == "\\r"    : decoded += "\r"; i+=2
        elif s[i:i+2] == "\\n"    : decoded += "\n"; i+=2
        elif s[i:i+2] == "\\x"    : decoded += chr(int(s[i+2:i+4], 16)); i+=4
        elif s[i:i+2] == "\\u"    : decoded += chr(int(s[i+2:i+6], 16)); i+=6
        elif s[i:i+2] == "\\U"    : decoded += chr(int(s[i+2:i+10], 16)); i+=10
        elif s[i:i+1] == "\\"     : raise LE_SyntaxError(f"Invalid backslash sequence in string at position {i}")
        else                      : decoded += s[i]; i+=1

    return decoded


def _encodeString(s):
    encoded = ""

    for c in s:
        if   c == "\\" : encoded += "\\\\"
        elif c == "\"" : encoded += "\\\""
        else           : encoded += c

    return encoded


##############################################################################
# BUILTIN FUNCTIONS

class LE_Function:
    def __init__(self, fn, **kwargs):
        self.fn = fn
        self.opts = {
            "minargs"    : kwargs.get("minargs", kwargs.get("nargs", 0)),
            "maxargs"    : kwargs.get("maxargs", kwargs.get("nargs", float("Inf"))),
            "delayvisit" : kwargs.get("delayvisit", False),
        }

        # Validation
        if   self.opts["minargs"] > self.opts["maxargs"]:
            raise LE_SyntaxError(f"minargs ({self.opts['minargs']}) is greater than than maxargs ({self.opts['maxargs']})")

    def __call__(self, *args, **kwargs):
        minargs = self.opts["minargs"]
        maxargs = self.opts["maxargs"]

        if   len(args) < minargs or maxargs < len(args):
            raise LE_SyntaxError(f"Invalid argument count; expected [{minargs}, {maxargs}], got {len(args)}")

        return self.fn(*args, **kwargs)


def __builtin_ceil(value, **kwargs):
    return LE_Int(math.ceil(value))


def __builtin_eval(value, **kwargs):
    return eval(value, kwargs["sym"])


def __builtin_floor(value, **kwargs):
    return LE_Int(math.floor(value))


def __builtin_for(init, cond, incr, block, **kwargs):
    visitor = kwargs["visitor"]
    result = LE_Int(0)

    visitor.visit(init)

    while(visitor.visit(cond).value):
        result = visitor.visit(block)
        visitor.visit(incr)

    return result


def __builtin_if(*args, **kwargs):
    visitor = kwargs["visitor"]
    result = LE_Int(0)
    i = 0

    while i+1 < len(args):
        if visitor.visit(args[i]).value:
            result = visitor.visit(args[i+1])
            break

        i += 2

    if i+1 == len(args):
        result = visitor.visit(args[-1])

    return result


def __builtin_len(value, **kwargs):
    return LE_Int(len(value))


def __builtin_print(*args, **kwargs):
    print(*[x.value for x in args])

    return LE_Int(len(args))


def __builtin_round(value, **kwargs):
    return LE_Int(round(value))


def __builtin_sqrt(value, **kwargs):
    return LE_Double(math.sqrt(value))


def __builtin_while(cond, expr, **kwargs):
    visitor = kwargs["visitor"]
    result = LE_Int(0)

    while(visitor.visit(cond).value):
        result = visitor.visit(expr)

    return result


builtins = {
    "CEIL"  : LE_Function(__builtin_ceil , nargs=1                   ),
    "EVAL"  : LE_Function(__builtin_eval , nargs=1                   ),
    "FLOOR" : LE_Function(__builtin_floor, nargs=1                   ),
    "FOR"   : LE_Function(__builtin_for  , nargs=4  , delayvisit=True),
    "IF"    : LE_Function(__builtin_if   , minargs=2, delayvisit=True),
    "LEN"   : LE_Function(__builtin_len  , nargs=1                   ),
    "PRINT" : LE_Function(__builtin_print                            ),
    "ROUND" : LE_Function(__builtin_round, nargs=1                   ),
    "SQRT"  : LE_Function(__builtin_sqrt , nargs=1                   ),
    "WHILE" : LE_Function(__builtin_while, nargs=2  , delayvisit=True),
}

