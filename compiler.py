import hllparser as hll
import sys

i=0
class Compiler:
    def traversal(self,node):
        if type(node) == hll.Print:
            self.t_print(node)
        elif type(node) == hll.Int:
            self.t_int(node)
        elif type(node) == hll.Bin_Op:
            self.t_binOP(node)
        elif type(node) == hll.Assign:
            self.t_assign(node)
        elif type(node) == hll.Var:
            self.t_var(node)
        elif type(node) ==hll.While:
            self.t_while(node)    
    def t_print(self, node):
        self.traversal(node.exp)
        print ("PRINT")
    def t_int(self, node):
        print("INT", node.val)
    def t_binOP(self,node):
        self.traversal(node.lhs)
        self.traversal(node.rhs)
        if node.op == '+':
            print("ADD")
        elif node.op == "<":
            print("LESS_THAN")
        elif node.op ==">":
            print("GREATER_THAN")
        elif node.op == "==":
            print("EQUALS")            
    def t_assign(self, node):
        self.traversal(node.exp)                
        print("VAR_SET", node.name)
    def t_var(self, node):
        print("VAR_LOOKUP", node.name)
    def t_while(self,node):
        global i
        sys.stdout.write("label" + str(i) + ": ")
        self.traversal(node.cond)
        print("JEQ","label" + str(i+1))
        for e in node.body:
           self.traversal(e)
        print("VAR_LOOKUP", node.cond.lhs.name)
        print("JGE","label" + str(i))
        i = i+1 
        sys.stdout.write("label" + str(i) + ": ")


if __name__ == "__main__":
    tree = []
    p = hll.parse(open(sys.argv[1], "r").read())
    for e in p:
        Compiler().traversal(e)
    print("EXIT")    
