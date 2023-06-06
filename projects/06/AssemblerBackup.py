import sys
import re
import os


filename = sys.argv[1]
filename_split, _ = filename.split('.')
new_filename = filename_split + '1.hack'

with open(filename, 'r') as asm:
    raw_contents = asm.readlines()

def no_symbol_cleanup(filename):
    # Returns a commands_list that has all the raw commands without any comments or linebreaks
    symbol_table = {
                'SP' : '0',
                'LCL' : '1',
                'ARG' : '2',
                'THIS' : '3',
                'THAT' : '4',
                'R0' : '0',
                'R1' : '1',
                'R2' : '2',
                'R3' : '3',
                'R4' : '4',
                'R5' : '5',
                'R6' : '6',
                'R7' : '7',
                'R8' : '8',
                'R9' : '9',
                'R10' : '10',
                'R11' : '11',
                'R12' : '12',
                'R13' : '13',
                'R14' : '14',
                'R15' : '15',
                'SCREEN' : '16384',
                'KBD' : '24576',
            }

    comment_free = []
    for line in filename:
        comment_free.append(re.sub("//.*$\n", "", line))

    newline_free = []
    for line in comment_free:
        newline_free.append(re.sub("\n", "", line))

    commands_list = []
    added = []
    command_location = 0
    for line in newline_free:
        line = line.replace(' ', '')
        addline = line.replace('@', '').replace('(','').replace(')','')
        if len(line) != 0:
            if  '(' in line and addline not in added:
                key = line.replace('(','').replace(')','')
                symbol_table_value = str(command_location)
                symbol_table[key] = symbol_table_value
                added.append(key)
            elif re.match('@[^0-9]+.*', line) and addline not in added:
                _, key = line.split('@')
                symbol_table_value = str(command_location)
                symbol_table[key] = symbol_table_value
                added.append(key)
                commands_list.append(line)
            elif '(' not in line:
                commands_list.append(line)
            #if '(' not in line:
            #    command_location += 1
        print(commands_list)

    instruction_list = []
    for line in commands_list:
        if len(line) != 0:
            if re.match('@[^0-9]+.*', line):
                _, key = line.split('@')
                instruction = '@' + symbol_table.get(key)
                instruction_list.append(instruction)
            else:
                instruction_list.append(line)

    clean_instruction_list = []
    for line in instruction_list:
        line = line.replace(' ', '')
        clean_instruction_list.append(line)

    print(newline_free, clean_instruction_list, symbol_table)
    return clean_instruction_list, symbol_table

def a_command_translate(a_command, symbol_table):
    # Gets the value of the A-Command and translates it to its padded binary equivalent
    if re.match('@[^0-9]+.*', a_command):
        _, key = a_command.split('@')
        print(a_command, key)
        instruction = symbol_table.get(key)
        print(instruction)
        value_int = int(instruction)
        bin_command = f'{value_int:016b}'
    else:
        _, constant = a_command.split('@')
        constant_int = int(constant)
        bin_command = f'{constant_int:016b}'

    return bin_command

def c_command_translate(c_command):
    # Gets the value of the C-Command and translates it to its padded binary equivalent
    print(c_command)
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

    print(bin_string)
    return bin_string

def build_binary_list(commands_list, symbol_table):
    bin_commandlist = []
    for command in commands_list:
        if command[0] == '@':
            bin_command = a_command_translate(command, symbol_table)
            bin_commandlist.append(bin_command)
        else:
            bin_command = c_command_translate(command)
            bin_commandlist.append(bin_command)

    return bin_commandlist

commands_list, symbol_table = no_symbol_cleanup(raw_contents)
bin_commandlist = build_binary_list(commands_list, symbol_table)
hack_binary = '\n'.join(bin_commandlist)

with open(new_filename, 'w') as hack:
    hack.write(hack_binary)
