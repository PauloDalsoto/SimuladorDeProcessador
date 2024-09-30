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
        pass

    def memory_access(self):
        instruction = self.stages['EX']
        self.stages['MEM'] = instruction
        pass
    
    def execute(self):
        instruction = self.stages['ID']
        self.stages['EX'] = instruction
        pass

    def decode(self):
        # se o estagio anterior nao for done
        instruction = (self.stages['IF'] if self.stages['IF'] and self.stages['IF'].opcode != "done" else None)
        self.stages['ID'] = instruction
        pass
    
    def instruction_fetch(self):
        # Verifica se ainda há instruções a serem buscadas
        if self.instruction_index < len(self.instruction_memory):
            instr_data = self.instruction_memory[self.instruction_index].split()

            # Obtém o opcode e os operandos
            opcode = instr_data[0]
            oper1  = instr_data[1] if len(instr_data) > 1 else None
            oper2  = instr_data[2] if len(instr_data) > 2 else None
            oper3  = instr_data[3] if len(instr_data) > 3 else None

            self.instruction_index += 1
            instruction = Instruction(opcode, oper1, oper2, oper3)
            
            self.stages['IF'] = instruction



    def clock(self):
        self.clock_cycle += 1
        
        self.write_back()
        self.memory_access()
        self.execute()
        self.decode()
        self.instruction_fetch()
