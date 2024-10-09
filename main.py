import simulador_pipeline.pipeline as pipeline
import simulador_pipeline.load_program as load_program
import simulador_pipeline.register_file as register_file
import simulador_pipeline.load_program 

def print_status(instructions, pipeline_processor):
    # Exibe o ciclo de clock atual
    print(f" CICLO DE CLOCK: {pipeline_processor.clock_cycle} ".center(40, '-'))
    
    # Exibe o conteúdo dos registradores
    print(f" ESTADO DOS REGISTRADORES ".center(40, '='))
    for i in range(0, 32, 4):
        print(f"R{i:02}: {pipeline_processor.registers.read(i)}\tR{i+1:02}: {pipeline_processor.registers.read(i+1)}\tR{i+2:02}: {pipeline_processor.registers.read(i+2)}\tR{i+3:02}: {pipeline_processor.registers.read(i+3)}")
    
    # Exibe a memória de instruções
    print('\n')
    print(f" MEMÓRIA DE INSTRUÇÕES ".center(40, '='))
    for i, instr in enumerate(instructions):
        print(f"Instrução {i:02}: {instr}")

    # Exibe o estado do pipeline
    print('\n')
    print(f" ESTÁGIOS DO PIPELINE ".center(40, '='))
    stages = ['Instruction Fetch', 'Decode', 'Execution', 'Memory Access', 'Write Back']
    max_opcode_length = 17
    max_oper_length = 11 

    for stage, instr in zip(stages, pipeline_processor.get_pipeline_stages()):
        if stage == 'Instruction Fetch':  # Ajuste para o estágio de Fetch
            if instr:
                print(f"{stage:<{max_opcode_length}}: '{instr:<{max_oper_length}}'")
            else:
                print(f"{stage:<{max_opcode_length}}: (Vazio)")
        else:
            # Ajuste para outros estágios
            if instr:
                print(f"{stage:<{max_opcode_length}}: {instr.opcode:<{max_oper_length}} | "
                      f"Oper1: {instr.oper1 if instr.oper1 is not None else '':<{max_oper_length}} | "
                      f"Oper2: {instr.oper2 if instr.oper2 is not None else '':<{max_oper_length}} | "
                      f"Oper3: {instr.oper3 if instr.oper3 is not None else '':<{max_oper_length}}| "
                      f"Valida: {instr.valida}")
            else:
                print(f"{stage:<{max_opcode_length}}: (Vazio)")
            
    print('\n')
    print(f"".center(40, '-'))

def main():
    instruction_memory, data_memory, label_map  = load_program.load_program('program.txt')
    registers = register_file.RegisterFile()
    pipeline_processor = pipeline.Pipeline(registers,
                                           instruction_memory,
                                           data_memory,
                                           label_map)
    
    while True:
        input("Pressione enter para avançar um ciclo de clock...")
        pipeline_processor.clock()
        print_status(instruction_memory, pipeline_processor)

if __name__ == "__main__":
    main()
