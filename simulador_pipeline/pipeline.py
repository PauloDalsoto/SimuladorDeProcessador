from .instruction import Instruction

class Pipeline:
    def __init__(self, registers, instruction_memory, data_memory, label_map, prediction):
        self.registers = registers
        self.instruction_memory = instruction_memory
        self.data_memory = data_memory
        self.label_map = label_map
        
        self.clock_cycle = 0
        self.instruction_index = 0
        self.old_instruction_index = 0
        
        self.beq_flag = False
        self.beq_jump = 0
        self.beq_jump_index = 0
        
        self.prediction = prediction
        self.predict_table = [0] * len(instruction_memory)
        self.instruction_valid = 0
        self.instruction_invalid = 0
        
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
        
        if instruction and instruction.valida:
            self.instruction_valid += 1
            match instruction.opcode:
                case 'add':
                    oper3 = instruction.oper3[1:]
                    self.registers.write(oper3, instruction.temp1)
                
                case 'sub':
                    oper3 = instruction.oper3[1:]
                    self.registers.write(oper3, instruction.temp1)
                    
                case 'lw':
                    oper2 = instruction.oper2[1:]
                    self.registers.write(oper2, instruction.temp1)    
        elif instruction:
            self.instruction_invalid += 1
            
    def memory_access(self):
        instruction = self.stages['EX']
        self.stages['MEM'] = instruction
        
        if instruction and instruction.valida:
            match instruction.opcode:
                case 'sw':
                    self.data_memory[int(instruction.temp1)] = self.registers.read(instruction.oper2[1:])
                    self.label_map[instruction.temp3] = instruction.temp1
    
    def execute(self):
        instruction = self.stages['ID']
        self.stages['EX'] = instruction
        
        if instruction and instruction.valida:
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
                    oper3 = self.data_memory[self.label_map[instruction.oper3]]
                    instruction.temp1 = oper1 + oper3
                
                case 'sw':
                    oper1 = self.registers.read(instruction.oper1[1:])
                    oper3 = self.registers.read(instruction.oper3)
                    instruction.temp1 = oper1 + oper3
                    
                case 'beq':
                    oper1 = self.registers.read(instruction.oper1[1:])
                    oper2 = self.registers.read(instruction.oper2[1:])
                    if oper1 == oper2:
                        self.beq_jump_index = int(instruction.oper3)
                        self.beq_flag = True
                        
                        if self.prediction:
                            if self.predict_table[self.instruction_index - 2] == 1 or self.predict_table[self.old_instruction_index - 1] == 1:
                                self.beq_jump = 0
                                self.beq_flag = False
                            else:
                                self.predict_table[self.instruction_index - 2] = 1
                            

    def decode(self):
        if_instr = self.stages['IF']
        
        if if_instr:
            if 'done' in if_instr:
                opcode = if_instr
                instruction = Instruction(opcode, None, None, None)
            else:     
                instr_data = if_instr.split() 
                opcode = instr_data[0]
                oper1  = instr_data[1] if len(instr_data) > 1 else None
                oper2  = instr_data[2] if len(instr_data) > 2 else None
                oper3  = instr_data[3] if len(instr_data) > 3 else None

                instruction = Instruction(opcode, oper1, oper2, oper3)
                if instruction.opcode == 'sw':
                    instruction.temp3 = instr_data[4] if len(instr_data) > 4 else None                                    
        else:
            instruction = None
            
        if self.beq_flag:
            self.beq_jump += 1
            
            if self.beq_jump == 2:
                self.beq_jump = 0
                self.beq_flag = False
                
            if if_instr:
                instruction.valida = False
            
        
        self.stages['ID'] = instruction
        
        
    def instruction_fetch(self):
        if self.prediction and self.predict_table[self.instruction_index - 1] == 1:             
            self.old_instruction_index = self.instruction_index
            self.instruction_index = self.beq_jump_index
            
            instr_raw = self.instruction_memory[self.instruction_index]
            self.stages['IF'] = instr_raw 
            self.instruction_index += 1
            return
                
        if self.instruction_index < len(self.instruction_memory):
            instr_raw = self.instruction_memory[self.instruction_index]
            self.instruction_index += 1
            self.stages['IF'] = instr_raw                
        else:
            self.stages['IF'] = None
        
        if self.beq_jump == 1:
            self.instruction_index = self.beq_jump_index
           
            
    def clock(self):
        self.clock_cycle += 1
        
        self.write_back()
        self.memory_access()
        self.execute()
        self.decode()
        self.instruction_fetch()
