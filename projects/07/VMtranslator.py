import sys
import re
import os


filename = sys.argv[1]
filename_split, _ = filename.split('.')
new_filename = filename_split + '.asm'

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

def arithmetic_command(instruction):

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
                     'M=M+1']

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
                     'M=M+1']

            'neg' : ['@SP',
                     'AM=M-1',
                     'M=-M',
                     '@SP',
                     'M=M+1']

            }

    asm_instructions_list = arithmetic_key.get(instruction)
    asm_instructions = '\n'.join(asm_instructions_list)


    return asm_instructions

def push_pop_command(instruction):

    if instruction[1] == 'constant':
        constant = '@' + instruction[2]
        asm_instructions_list = [constant,
                            'D=A',
                            '@SP',
                            'A=M',
                            'M=D',
                            '@SP',
                            'M=M+1']

    asm_instructions = '\n'.join(asm_instructions_list)

    return asm_instructions


def instruction_type(instructions_list):
    """ Parses each instruction and sends it to get parsed in the appropiate function
        """
    asm_instructions_list = []
    for instruction in instructions_list:
        instruction_comment = '//' + str(instruction)
        asm_instructions_list.append(instruction_comment)
        try:
            command, memory_segment, value = instruction.split(' ')
            parsed_instruction = (command, memory_segment, value)
            asm_instructions = push_pop_command(parsed_instruction)
            asm_instructions_list.append(asm_instructions)
        except:
            asm_instructions = arithmetic_command(instruction)
            asm_instructions_list.append(asm_instructions)
        print(asm_instructions_list)

    return asm_instructions_list


def a_command_translate(a_command, symbol_table):
    # Gets the value of the A-Command and translates it to its padded binary equivalent
    if re.match('@[^0-9]+.*', a_command):
        _, key = a_command.split('@')
        instruction = symbol_table.get(key)
        value_int = int(instruction)
        bin_string = f'{value_int:016b}'
    else:
        _, constant = a_command.split('@')
        constant_int = int(constant)
        bin_string = f'{constant_int:016b}'

    return bin_string

def c_command_translate(c_command):
    # Gets the value of the C-Command and translates it to its padded binary equivalent
    bin_string = '111'
    jump_bits_translate = {
                'null' : '000',
                'JGT' : '001',
                'JEQ' : '010',
                'JGE' : '011',
                'JLT' : '100',
                'JNE' : '101',
                'JLE' : '110',
                'JMP' : '111',
            }

    dest_bits_translate = {
                'null' : '000',
                'M' : '001',
                'D' : '010',
                'MD' : '011',
                'DM' : '011',
                'A' : '100',
                'AM' : '101',
                'MA' : '101',
                'AD' : '110',
                'DA' : '110',
                'AMD' : '111',
                'ADM' : '111',
                'DAM' : '111',
                'DMA' : '111',
                'MAD' : '111',
                'MDA' : '111',
            }

    comp_bits_translate = {
                '0' : '0101010',
                '1' : '0111111',
                '-1' : '0111010',
                'D' : '0001100',
                'A' : '0110000',
                '!D' : '0001101',
                '!A' : '0110001',
                '-D' : '0001111',
                '-A' : '0110011',
                'D+1' : '0011111',
                'A+1' : '0110111',
                'D-1' : '0001110',
                'A-1' : '0110010',
                'D+A' : '0000010',
                'D-A' : '0010011',
                'A-D' : '0000111',
                'D&A' : '0000000',
                'D|A' : '0010101',
                'M' : '1110000',
                '!M' : '1110001',
                '-M' : '1110011',
                'M+1' : '1110111',
                'M-1' : '1110010',
                'D+M' : '1000010',
                'D-M' : '1010011',
                'M-D' : '1000111',
                'D&M' : '1000000',
                'D|M' : '1010101',
            }
    if ';' in c_command:
        comp_bits, jump_bits = c_command.split(';')
        jump_bin = jump_bits_translate.get(jump_bits)
        if '=' in comp_bits:
            dest_bits, comp_bits = comp_bits.split('=')
            comp_bin = comp_bits_translate.get(comp_bits)
            dest_bin = dest_bits_translate.get(dest_bits)
            bin_string = bin_string + comp_bin + dest_bin + jump_bin
        else:
            dest_bits = 'null'
            comp_bin = comp_bits_translate.get(comp_bits)
            dest_bin = dest_bits_translate.get(dest_bits)
            bin_string = bin_string + comp_bin + dest_bin + jump_bin

    elif '=' in c_command:
        jump_bits = 'null'
        jump_bin = jump_bits_translate.get(jump_bits)
        dest_bits, comp_bits = c_command.split('=')
        comp_bin = comp_bits_translate.get(comp_bits)
        dest_bin = dest_bits_translate.get(dest_bits)
        bin_string = bin_string + comp_bin + dest_bin + jump_bin

    else:
        jump_bits = 'null'
        dest_bits = 'null'
        comp_bits = c_command
        jump_bin = jump_bits_translate.get(jump_bits)
        dest_bin = dest_bits_translate.get(dest_bits)
        comp_bin = comp_bits_translate.get(comp_bits)
        bin_string = bin_string + comp_bin + dest_bin + jump_bin

    return bin_string

def build_asm_list(commands_list, symbol_table):
    bin_commandlist = []
    for command in commands_list:
        if command[0] == '@':
            bin_command = a_command_translate(command, symbol_table)
            bin_commandlist.append(bin_command)
        else:
            bin_command = c_command_translate(command)
            bin_commandlist.append(bin_command)

    return asm_commandlist

instructions_list = instruction_cleanup(raw_contents)
asm_commands_list = instruction_type(instructions_list)
#commands_list, symbol_table = instruction_cleanup(raw_contents)
#asm_commands_list = build_asm_list(commands_list, symbol_table)
print(asm_commands_list)
assembly_instructions = '\n'.join(asm_commands_list)

with open(new_filename, 'w') as asm:
    asm.write(assembly_instructions)
