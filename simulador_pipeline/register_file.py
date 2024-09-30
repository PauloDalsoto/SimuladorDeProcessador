class RegisterFile:
    def __init__(self):
        self.registers = [0] * 32  
        self.registers[0] = 0
    
    def read(self, reg_num):
        return self.registers[reg_num]
    
    def write(self, reg_num, value):
        if reg_num != 0:
            self.registers[reg_num] = value
