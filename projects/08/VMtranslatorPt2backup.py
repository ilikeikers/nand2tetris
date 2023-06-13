import sys
import re
import os


filename = sys.argv[1]
filename_split, _ = filename.split('.')
NEW_FILENAME = filename_split + '.asm'
STATIC_VARIABLE_ROOT = filename_split + '.'

with open(filename, 'r') as raw_vm:
    raw_contents = raw_vm.readlines()

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
    asm_instructions = '\n'.join(asm_instructions_list)
    if instruction in ['gt', 'lt', 'eq']:
        command_count += 1

    return asm_instructions, command_count

def translate_memory_command(command_type, memory_segment, value):

    memory_destination = translate_memory_segment(command_type, memory_segment, value)
    command_instruction = translate_push_pop(command_type)

    asm_instructions_list = memory_destination + command_instruction
    asm_instructions = '\n'.join(asm_instructions_list)

    return asm_instructions

def translate_branching_command(command_type, branch_name, value, call_count):

    asm_instructions = ''
    if command_type == 'label':
        asm_instructions = '(' + branch_name + ')'

    elif command_type == 'goto':
        asm_branch_name = '@' + str(branch_name)
        asm_instructions_list = [asm_branch_name,
                                 '0;JMP']
        asm_instructions = '\n'.join(asm_instructions_list)

    elif command_type == 'if-goto':
        asm_branch_name = '@' + str(branch_name)
        asm_instructions_list = ['@SP',
                                 'AM=M-1',
                                 'D=M',
                                 asm_branch_name,
                                 'D;JNE']
        asm_instructions = '\n'.join(asm_instructions_list)

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

        asm_instructions = '\n'.join(asm_instructions_list)

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
        asm_instructions = '\n'.join(asm_instructions_list)

    return asm_instructions, call_count

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
        print(vm_instruction)
        instruction_comment = '//' + str(vm_instruction)
        asm_instructions_list.append(instruction_comment)
        try:
            command_type, memory_segment, value = vm_instruction.split(' ')
            newstring = vm_instruction.split(' ')
            if (command_type == 'call') or (command_type == 'function'):
                asm_instructions, call_count = translate_branching_command(command_type, memory_segment, value, call_count)
            else:
                asm_instructions = translate_memory_command(command_type, memory_segment, value)
            asm_instructions_list.append(asm_instructions)
        except:
            try:
                command_type, branch_name = vm_instruction.split(' ')
                asm_instructions, _ = translate_branching_command(command_type, branch_name, *_)
                asm_instructions_list.append(asm_instructions)
            except:
                asm_instructions, command_count = translate_arithmetic_command(vm_instruction, command_count)
                asm_instructions_list.append(asm_instructions)

    return asm_instructions_list

instructions_list = instruction_cleanup(raw_contents)
asm_commands_list = build_asm_instructions_list(instructions_list)
print(asm_commands_list)
assembly_instructions = '\n'.join(asm_commands_list)

with open(NEW_FILENAME, 'w') as asm:
    asm.write(assembly_instructions)
