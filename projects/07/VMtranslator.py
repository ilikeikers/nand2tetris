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
    """ Returns an instruction list that has all the raw commands without any comments or linebreaks
        """
    comment_free = []
    for line in raw_contents:
        comment_free.append(re.sub("//.*$\n", "", line))

    instruction_list = []
    for line in comment_free:
        instruction_list.append(re.sub("\n", "", line))

    clean_instruction_list = []
    for line in instruction_list:
        if len(line) != 0:
            clean_instruction_list.append(line)

    return clean_instruction_list

def translate_arithmetic_command(instruction, command_count):

    count = str(command_count)

    arithmetic_key = {

            'add' : ['@SP',
                     'AM=M-1',
                     'D=M',
                     '@SP',
                     'AM=M-1',
                     'D=D+M',
                     '@SP',
                     'A=M',
                     'M=D',
                     '@SP',
                     'M=M+1'],

            'sub' : ['@SP',
                     'AM=M-1',
                     'D=M',
                     '@SP',
                     'AM=M-1',
                     'D=M-D', # might need to change M and D order
                     '@SP',
                     'A=M',
                     'M=D',
                     '@SP',
                     'M=M+1'],

            'neg' : ['@SP',
                     'AM=M-1',
                     'M=-M',
                     '@SP',
                     'M=M+1'],

            'not' : ['@SP',
                     'AM=M-1',
                     'M=!M',
                     '@SP',
                     'M=M+1'],

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
                     '@SP',
                     'AM=M-1',
                     'D=D&M',
                     '@SP',
                     'A=M',
                     'M=D',
                     '@SP',
                     'M=M+1'],


            'or' : ['@SP',
                    'AM=M-1',
                    'D=M',
                    '@SP',
                    'AM=M-1',
                    'D=D|M',
                    '@SP',
                    'A=M',
                    'M=D',
                    '@SP',
                    'M=M+1']

            }

    asm_instructions_list = arithmetic_key.get(instruction)
    asm_instructions = '\n'.join(asm_instructions_list)
    if instruction in ['gt', 'lt', 'eq']:
        command_count += 1

    return asm_instructions, command_count

def translate_memory_command(instruction):

    command_instruction = translate_push_pop_segment(instruction[0])
    memory_destination = translate_memory_segment(instruction[0], instruction[1], instruction[2])

    asm_instructions_list = memory_destination + command_instruction
    asm_instructions = '\n'.join(asm_instructions_list)

    return asm_instructions

def translate_push_pop_segment(command):

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

def instruction_type(instructions_list):
    """ Parses each instruction and sends it to get parsed in the appropiate function
        """
    asm_instructions_list = []
    command_count = 0
    for instruction in instructions_list:
        instruction_comment = '//' + str(instruction)
        asm_instructions_list.append(instruction_comment)
        try:
            command, memory_segment, value = instruction.split(' ')
            parsed_instruction = (command, memory_segment, value)
            asm_instructions = translate_memory_command(parsed_instruction)
            asm_instructions_list.append(asm_instructions)
        except:
            asm_instructions, command_count = translate_arithmetic_command(instruction, command_count)
            asm_instructions_list.append(asm_instructions)

    return asm_instructions_list

instructions_list = instruction_cleanup(raw_contents)
asm_commands_list = instruction_type(instructions_list)
print(asm_commands_list)
assembly_instructions = '\n'.join(asm_commands_list)

with open(NEW_FILENAME, 'w') as asm:
    asm.write(assembly_instructions)
