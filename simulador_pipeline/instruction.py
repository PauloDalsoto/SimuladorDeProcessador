class Instruction:
    def __init__(self, opcode, oper1, oper2, oper3):
        self.opcode = opcode
        self.oper1 = oper1
        self.oper2 = oper2
        self.oper3 = oper3
        self.temp1 = None
        self.temp2 = None
        self.temp3 = None
        self.valida = True