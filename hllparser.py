import re, sys

RE_ID = re.compile("[a-zA-Z_][a-zA-Z_0-9]*")
RE_INT = re.compile("[0-9]+")

class Assign(object):
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def pp(self):
        return "%s = %s;" % (self.name, self.exp.pp())

class Int(object):
    def __init__(self, val):
        self.val = val

    def pp(self):
        return self.val

class Var(object):
    def __init__(self, name):
        self.name = name

    def pp(self):
        return self.name

class Bin_Op(object):
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def pp(self):
        return "%s %s %s" % (self.lhs.pp(), self.op, self.rhs.pp())

class While(object):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def pp(self):
        return "while %s {\n  %s\n}" % (self.cond.pp(), "\n  ".join([x.pp() for x in self.body]))

class Print(object):
    def __init__(self, exp):
        self.exp = exp

    def pp(self):
        return "print %s;" % self.exp.pp()

def parse(s):
    i = 0
    p = []
    while i < len(s):
        i = skip_ws(s, i)
        if i == len(s):
            break
        r = parse_stmt(s, i)
        if r is not None:
            p.append(r[0])
            i = r[1]
            continue
        print("Unknown syntax at position", i)
        print(s[i:s.index("\n", i)])
        sys.exit(1)
    return p

def parse_stmt(s, i):
    r = parse_assign(s, i)
    if r is not None:
        return r
    r = parse_while(s, i)
    if r is not None:
        return r
    r = parse_print(s, i)
    if r is not None:
        return r
    return

def skip_ws(s, i):
    while i < len(s) and s[i] in " \t\n\r":
        i += 1
    return i

def parse_assign(s, i):
    m = RE_ID.match(s, i)
    if m is None:
        return
    varn = m.group(0) # var name
    i += len(varn)
    i = skip_ws(s, i)
    if i < len(s) and s[i] != "=":
        return None
    i += 1
    i = skip_ws(s, i)
    r = parse_expr(s, i)
    if r is None:
        return
    exp, i = r
    i = skip_ws(s, i)
    if i == len(s) or s[i] != ";":
        return
    i += 1
    return Assign(varn, exp), i

OPS = ["<", ">", "+", "-", "=="]
def parse_expr(s, i):
    m = RE_INT.match(s, i)
    if m is not None:
        lhs = Int(m.group(0))
        i += len(m.group(0))
    else:
        m = RE_ID.match(s, i)
        if m is None:
            return
        lhs = Var(m.group(0))
        i += len(m.group(0))
    i = skip_ws(s, i)
    if i == len(s):
        return lhs, i

    for op in OPS:
        if s.startswith(op, i):
            break
    else:
        return lhs, i
    i += len(op)
    i = skip_ws(s, i)
    r = parse_expr(s, i)
    if r is None:
        return
    rhs, i = r
    return Bin_Op(op, lhs, rhs), i

def parse_while(s, i):
    if not s.startswith("while", i):
        return
    i += len("while")
    i = skip_ws(s, i)
    r = parse_expr(s, i)
    if r is None:
        return
    cond, i = r
    i = skip_ws(s, i)
    if i == len(s) or s[i] != "{":
        return
    i += 1
    body = []
    while i < len(s):
        i = skip_ws(s, i)
        r = parse_stmt(s, i)
        if r is not None:
            body.append(r[0])
            i = r[1]
            continue
        if i == len(s) or s[i] != "}":
            return
        break
    i += 1
    return While(cond, body), i

def parse_print(s, i):
    if not s.startswith("print", i):
        return
    i += len("print")
    i = skip_ws(s, i)
    r = parse_expr(s, i)
    if r is None:
        return
    exp, i = r
    i = skip_ws(s, i)
    if i == len(s) or s[i] != ";":
        return
    i += 1
    return Print(exp), i


if __name__ == "__main__":
    p = parse(open(sys.argv[1], "r").read())
    for e in p: 
       print(e.pp())