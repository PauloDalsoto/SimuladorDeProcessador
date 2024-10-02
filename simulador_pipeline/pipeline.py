from .instruction import Instruction

class Pipeline:
    def __init__(self, registers, instruction_memory, data_memory, label_map):
        self.registers = registers
        self.instruction_memory = instruction_memory
        self.data_memory = data_memory
        self.label_map = label_map
    
        self.clock_cycle = 0
        self.instruction_index = 0
        
        # Estágios do pipeline
        self.stages = {
            'IF': None,
            'ID': None,
            'EX': None,
            'MEM': None,
            'WB': None
        }
    
    def get_pipeline_stages(self):
        return [self.stages['IF'], self.stages['ID'], self.stages['EX'], self.stages['MEM'], self.stages['WB']]

    def write_back(self):
        instruction = self.stages['MEM']
        self.stages['WB'] = instruction
        
        if instruction:
            match instruction.opcode:
                case 'add':
                    oper3 = instruction.oper3[1:]
                    self.registers.write(oper3, instruction.temp1)
                    print(f'write back -> Valor de {instruction.oper3}: {instruction.temp1}')
                
                case 'sub':
                    oper3 = instruction.oper3[1:]
                    self.registers.write(oper3, instruction.temp1)
                    
                case 'lw':
                    oper2 = instruction.oper2[1:]
                    self.registers.write(oper2, instruction.temp1)    

    def memory_access(self):
        instruction = self.stages['EX']
        self.stages['MEM'] = instruction
        
        if instruction:
            match instruction.opcode:
                case 'lw':
                    instruction.temp1 = self.data_memory[self.label_map[instruction.oper3]]
                    print(f'mem acces -> Valor de {instruction.oper3}: {instruction.temp1}')
    
    def execute(self):
        instruction = self.stages['ID']
        self.stages['EX'] = instruction
        
        if instruction:
            match instruction.opcode:
                case 'add':
                    oper1 = self.registers.read(instruction.oper1[1:])
                    oper2 = self.registers.read(instruction.oper2[1:])
                    instruction.temp1 = oper1 + oper2
                    
                case 'sub':
                    oper1 = self.registers.read(instruction.oper1[1:])
                    oper2 = self.registers.read(instruction.oper2[1:])
                    instruction.temp1 = oper1 - oper2
                    
                case 'lw':
                    oper1 = self.registers.read(instruction.oper1[1:])
                    oper2 = self.registers.read(instruction.oper2[1:])
                    instruction.temp1 = oper1 + oper2

    def decode(self):
        if_instr = self.stages['IF']
        
        if if_instr:
            if 'done' in if_instr:
                opcode = if_instr
                self.stages['ID'] = Instruction(opcode, None, None, None)
                return 
             
            instr_data = if_instr.split() 
            opcode = instr_data[0]
            oper1  = instr_data[1] if len(instr_data) > 1 else None
            oper2  = instr_data[2] if len(instr_data) > 2 else None
            oper3  = instr_data[3] if len(instr_data) > 3 else None
            instruction = Instruction(opcode, oper1, oper2, oper3)
        else:
            instruction = None
        
        self.stages['ID'] = instruction
        
    def instruction_fetch(self):
        # Não busca novas instruções se 'done' já foi encontrado
        if self.instruction_index < len(self.instruction_memory):
            instr_raw = self.instruction_memory[self.instruction_index]
            self.instruction_index += 1
            self.stages['IF'] = instr_raw
        else:
            self.stages['IF'] = None
            
    def clock(self):
        self.clock_cycle += 1
        
        self.write_back()
        self.memory_access()
        self.execute()
        self.decode()
        self.instruction_fetch()
