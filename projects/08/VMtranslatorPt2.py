import sys
import re
import os



def main():
    root = sys.argv[1]

    for file in os.listdir(root):
        file_path = os.path.join(root, file)
        file_root = file_path.split('.')
        file_extension = file_root[1]
        file_directory = file_root[0]
        root_directory = file_directory.split('/')
        filename = root_directory[1]
        directory = root_directory[0]
        NEW_FILENAME = filename + '.asm'
        global STATIC_VARIABLE_ROOT
        STATIC_VARIABLE_ROOT = filename + '.'
        new_file = os.path.join(root, NEW_FILENAME)
        if file_extension == 'vm':
            with open(file_path, 'r') as raw_vm:
                raw_contents = raw_vm.readlines()

            call_sys_init_list, _ = translate_branching_command('call', 'Sys.init', 0, -1)
            sys_init_list = ['@256', 'D=A', '@SP', 'M=D', '// call Sys.init 0'] + call_sys_init_list + ['0;JMP']
            instructions_list = instruction_cleanup(raw_contents)
            asm_commands_list = build_asm_instructions_list(instructions_list)
            complete_asm_commands = sys_init_list + asm_commands_list
            assembly_instructions = '\n'.join(complete_asm_commands)


            with open(new_file, 'w') as asm:
                asm.write(assembly_instructions)

def instruction_cleanup(raw_contents):
    comment_free = []
    for line in raw_contents:
        comment_free.append(re.sub("\s*//.*$\n", "", line))

    instruction_list = []
    for line in comment_free:
        instruction_list.append(re.sub("\n", "", line))

    redo_instruction_list = []
    for line in instruction_list:
        redo_instruction_list.append(re.sub("\t", "", line))

    clean_instruction_list = []
    for line in redo_instruction_list:
        if line != '':
            clean_instruction_list.append(line)

    return clean_instruction_list

def translate_arithmetic_command(instruction, command_count):

    count = str(command_count)

    arithmetic_key = {

            'add' : ['@SP',
                     'AM=M-1',
                     'D=M',
                     'A=A-1',
                     'M=D+M'],

            'sub' : ['@SP',
                     'AM=M-1',
                     'D=M',
                     'A=A-1',
                     'M=M-D'],

            'neg' : ['@SP',
                     'A=M-1',
                     'M=-M'],

            'not' : ['@SP',
                     'A=M-1',
                     'M=!M'],

            'eq' : ['@SP',
                    'AM=M-1',
                    'D=M',
                    '@SP',
                    'AM=M-1',
                    'D=M-D',
                    '@TRUE_EQ' + count,
                    'D;JEQ',
                    '@FALSE_EQ' + count,
                    'D;JNE',
                    '(TRUE_EQ' + count + ')',
                    '@SP',
                    'A=M',
                    'M=-1',
                    '@PUSH_EQ' + count,
                    '0;JMP',
                    '(FALSE_EQ' + count + ')',
                    '@SP',
                    'A=M',
                    'M=0',
                    '(PUSH_EQ' + count + ')',
                    '@SP',
                    'M=M+1'],

            'gt' : ['@SP',
                    'AM=M-1',
                    'D=M',
                    '@SP',
                    'AM=M-1',
                    'D=M-D',
                    '@TRUE_GT' + count,
                    'D;JGT',
                    '@FALSE_GT' + count,
                    'D;JLE',
                    '(TRUE_GT' + count + ')',
                    '@SP',
                    'A=M',
                    'M=-1',
                    '@END_GT' + count,
                    '0;JMP',
                    '(FALSE_GT' + count + ')',
                    '@SP',
                    'A=M',
                    'M=0',
                    '(END_GT' + count + ')',
                    '@SP',
                    'M=M+1'],

            'lt' : ['@SP',
                    'AM=M-1',
                    'D=M',
                    '@SP',
                    'AM=M-1',
                    'D=M-D',
                    '@TRUE_LT' + count,
                    'D;JLT',
                    '@FALSE_LT' + count,
                    'D;JGE',
                    '(TRUE_LT' + count + ')',
                    '@SP',
                    'A=M',
                    'M=-1',
                    '@END_LT' + count,
                    '0;JMP',
                    '(FALSE_LT' + count + ')',
                    '@SP',
                    'A=M',
                    'M=0',
                    '(END_LT' + count + ')',
                    '@SP',
                    'M=M+1'],

            'and' : ['@SP',
                     'AM=M-1',
                     'D=M',
                     'A=A-1',
                     'M=D&M'],

            'or' : ['@SP',
                    'AM=M-1',
                    'D=M',
                    'A=A-1',
                    'M=D|M'],

            'return' : [# Set return address
                        '@LCL',
                        'D=M',
                        '@5',
                        'A=D-A',
                        'D=M',
                        '@R14',
                        'M=D',
                        # Recover saved frame
                        '@SP',
                        'A=M-1',
                        'D=M',
                        '@ARG',
                        'A=M',
                        'M=D',
                        'D=A+1',
                        '@SP',
                        'M=D',
                        '@LCL',
                        'AM=M-1',
                        'D=M',
                        '@THAT',
                        'M=D',
                        '@LCL',
                        'AM=M-1',
                        'D=M',
                        '@THIS',
                        'M=D',
                        '@LCL',
                        'AM=M-1',
                        'D=M',
                        '@ARG',
                        'M=D',
                        '@LCL',
                        'A=M-1',
                        'D=M',
                        '@LCL',
                        'M=D',
                        # Jump back to return address
                        '@R14',
                        'A=M',
                        '0;JMP']

            }

    asm_instructions_list = arithmetic_key.get(instruction)
    if instruction in ['gt', 'lt', 'eq']:
        command_count += 1

    return asm_instructions_list, command_count

def translate_memory_command(command_type, memory_segment, value):

    memory_destination = translate_memory_segment(command_type, memory_segment, value)
    command_instruction = translate_push_pop(command_type)

    asm_instructions_list = memory_destination + command_instruction

    return asm_instructions_list

def translate_branching_command(command_type, branch_name, value, call_count):

    if command_type == 'label':
        asm_instructions_list = ['(' + branch_name + ')']

    elif command_type == 'goto':
        asm_branch_name = '@' + str(branch_name)
        asm_instructions_list = [asm_branch_name,
                                 '0;JMP']

    elif command_type == 'if-goto':
        asm_branch_name = '@' + str(branch_name)
        asm_instructions_list = ['@SP',
                                 'AM=M-1',
                                 'D=M',
                                 asm_branch_name,
                                 'D;JNE']

    elif command_type == 'call':
        call_count += 1
        asm_return_address_name = '@retAddr_' + str(branch_name) + '.' + str(call_count)
        asm_return_address_label = '(' + 'retAddr_' + str(branch_name) + '.' + str(call_count) + ')'
        asm_function_address = '@' + str(branch_name)
        asm_value = '@' + str(value)
        asm_instructions_list = ['@SP',
                                 'D=M',
                                 '@R15',
                                 'M=D',
                                 asm_return_address_name,
                                 'D=A',
                                 '@SP',
                                 'A=M',
                                 'M=D',
                                 '@SP',
                                 'M=M+1',
                                 '@LCL',
                                 'D=M',
                                 '@SP',
                                 'A=M',
                                 'M=D',
                                 '@SP',
                                 'M=M+1',
                                 '@ARG',
                                 'D=M',
                                 '@SP',
                                 'A=M',
                                 'M=D',
                                 '@SP',
                                 'M=M+1',
                                 '@THIS',
                                 'D=M',
                                 '@SP',
                                 'A=M',
                                 'M=D',
                                 '@SP',
                                 'M=M+1',
                                 '@THAT',
                                 'D=M',
                                 '@SP',
                                 'A=M',
                                 'M=D',
                                 '@SP',
                                 'M=M+1',
                                 '@R15',
                                 'D=M',
                                 asm_value,
                                 'D=D-A',
                                 '@ARG',
                                 'M=D',
                                 '@SP',
                                 'D=M',
                                 '@LCL',
                                 'M=D',
                                 asm_function_address,
                                 '0;JMP',
                                 asm_return_address_label]


    elif command_type == 'function':
        asm_function_label = '(' + str(branch_name) + ')'
        value_count = int(value)
        initialize_LCL = []
        count = 0
        for count in range(value_count):
            initialize_LCL.append('M=0')
            initialize_LCL.append('A=A+1')
            count + 1
        asm_instructions_list = [asm_function_label, '@SP', 'A=M'] + initialize_LCL + ['D=A', '@SP', 'M=D']

    return asm_instructions_list, call_count

def translate_push_pop(command):

    asm_command = ''

    if str(command) == 'push':
        asm_command = ['@SP',
                       'A=M',
                       'M=D',
                       '@SP',
                       'M=M+1']
    else:
        asm_command = ['@R13',
                       'M=D',
                       '@SP',
                       'AM=M-1',
                       'D=M',
                       '@R13',
                       'A=M',
                       'M=D']

    return asm_command

def translate_memory_segment(command_type, memory_segment, value):

    offset = ['@' + str(value)] + ['D=A']

    if memory_segment == 'constant':
        memory_destination = []

    elif memory_segment == 'local':
        if command_type == 'pop':
            memory_destination = ['@LCL', 'D=M+D']
        elif command_type == 'push':
            memory_destination = ['@LCL', 'A=M+D', 'D=M']

    elif memory_segment == 'argument':
        if command_type == 'pop':
            memory_destination = ['@ARG', 'D=M+D']
        elif command_type == 'push':
            memory_destination = ['@ARG', 'A=M+D', 'D=M']

    elif memory_segment == 'this':
        if command_type == 'pop':
            memory_destination = ['@THIS', 'D=M+D']
        elif command_type == 'push':
            memory_destination = ['@THIS', 'A=M+D', 'D=M']

    elif memory_segment == 'that':
        if command_type == 'pop':
            memory_destination = ['@THAT', 'D=M+D']
        elif command_type == 'push':
            memory_destination = ['@THAT', 'A=M+D', 'D=M']

    elif memory_segment == 'temp':
        if command_type == 'pop':
            memory_destination = ['@R5', 'D=A+D']
        elif command_type == 'push':
            memory_destination = ['@R5', 'A=A+D', 'D=M']

    elif memory_segment == 'static':
        variable_name = '@' + STATIC_VARIABLE_ROOT + str(value)
        if command_type == 'pop':
            memory_destination = [variable_name, 'D=A']
        elif command_type == 'push':
            memory_destination = [variable_name, 'D=M']

    if memory_segment != ('pointer' or 'static'):
        memory_command = offset + memory_destination

    pointer_0 = (memory_segment == 'pointer') and (value == '0')
    pointer_1 = (memory_segment == 'pointer') and (value == '1')

    if pointer_0:
        if command_type == 'pop':
            memory_destination = ['@THIS', 'D=A']
        elif command_type == 'push':
            memory_destination = ['@THIS', 'D=M']
        memory_command = memory_destination

    if pointer_1:
        if command_type == 'pop':
            memory_destination = ['@THAT', 'D=A']
        elif command_type == 'push':
            memory_destination = ['@THAT', 'D=M']
        memory_command = memory_destination

    return memory_command

def build_asm_instructions_list(vm_instructions_list):

    asm_instructions_list = []
    command_count = 0
    call_count = 0
    for vm_instruction in vm_instructions_list:
        instruction_comment = '//' + str(vm_instruction)
        asm_instructions_list.append(instruction_comment)
        split_instruction = vm_instruction.split(' ')
        if len(split_instruction) == 3:
            command_type, memory_segment, value = split_instruction
            if (command_type == 'call') or (command_type == 'function'):
                asm_instructions, call_count = translate_branching_command(command_type, memory_segment, value, call_count)
                asm_instructions = '\n'.join(asm_instructions)
            else:
                asm_instructions = translate_memory_command(command_type, memory_segment, value)
                asm_instructions = '\n'.join(asm_instructions)
            asm_instructions_list.append(asm_instructions)
        if len(split_instruction) == 2:
            command_type, branch_name, *_ = split_instruction
            asm_instructions, _ = translate_branching_command(command_type, branch_name, _, _)
            asm_instructions = '\n'.join(asm_instructions)
            asm_instructions_list.append(asm_instructions)
        if len(split_instruction) == 1:
            asm_instructions, command_count = translate_arithmetic_command(vm_instruction, command_count)
            asm_instructions = '\n'.join(asm_instructions)
            asm_instructions_list.append(asm_instructions)

    return asm_instructions_list

main()
