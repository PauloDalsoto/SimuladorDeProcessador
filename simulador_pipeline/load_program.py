def load_program(filename):
    instructions = []
    data_memory = [0] * 256  
    data_index = 1 
    label_map = {} 
    
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                # Adiciona a instrução à lista de instruções

                # Verifica se a instrução contem'.fill'
                if '.fill' in stripped_line:
                    # Armazena o valor na próxima posição da memória de dados
                    data_memory[data_index] = int(stripped_line.split()[2])  # Pega o valor após o nome da variável
                    data_index += 1
                    label_map[stripped_line.split()[0]] = data_index
                else:
                    instructions.append(stripped_line)
    
    return instructions, data_memory, label_map
