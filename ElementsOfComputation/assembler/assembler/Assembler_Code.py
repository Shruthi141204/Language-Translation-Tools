#Defining the values of computation instructions
computation_dictionary = {
    "0" : "0101010",
    "1" : "0111111",
    "-1" : "0111010",
    "D" : "0001100",
    "A" : "0110000",
    "M" : "1110000",
    "!D" : "0001101",
    "!A" : "0110001",
    "!M" : "1110001",
    "-D" : "0001111",
    "-A" : "0110011",
    "-M" : "1110011",
    "D+1" : "0011111",
    "1+D" : "0011111",
    "A+1" : "0110111",
    "1+A" : "0110111",
    "M+1" : "1110111",
    "1+M" : "1110111",
    "D-1" : "0001110",
    "A-1" : "0110010",
    "M-1" : "1110010",
    "D+A" : "0000010",
    "A+D" : "0000010",
    "D+M" : "1000010",
    "M+D" : "1000010",
    "D-A" : "0010011",
    "A-D" : "0000111",
    "D-M" : "1010011",
    "M-D" : "1000111",
    "D&A" : "0000000",
    "D&M" : "1000000",
    "D|A" : "0010101",
    "D|M" : "1010101",
    "A&D" : "0000000",
    "M&D" : "1000000",
    "A|D" : "0010101",
    "M|D" : "1010101"
    }

#Defining the values of destination instructions
destination_dictionary = {
    'null':  '000',
    'M':   '001',
    'D':   '010',
    'MD':  '011',
    'DM':  '011',
    'A':   '100',
    'AM':  '101',
    'MA':  '101',
    'AD':  '110',
    'DA':  '110',
    'AMD': '111',
    'DMA': '111',
    'ADM': '111',
    'MAD': '111',
    'MDA': '111',
    'DAM': '111',
    }

#Defining the values of jump instructions
jump_dictionary = {
    'null':  '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    "JMP": '111',
    }

#Defining the values of different symbols
symbols = {
    'R0':'0000000000000000',
    'R1':'0000000000000001',
    'R2':'0000000000000010',
    'R3':'0000000000000011',
    'R4':'0000000000000100',
    'R5':'0000000000000101',
    'R6':'0000000000000110',
    'R7':'0000000000000111',
    'R8':'0000000000001000',
    'R9':'0000000000001001',
    'R10':'0000000000001010',
    'R11':'0000000000001011',
    'R12':'0000000000001100',
    'R13':'0000000000001101',
    'R14':'0000000000001110',
    'R15':'0000000000001111',
    'KBD':'0110000000000000',       #16384 in binary
    'SCREEN':'0100000000000000',    #24576 in binary
    'SP':'0000000000000000',
    'LCL':'0000000000000001',
    'ARG':'0000000000000010',
    'THIS':'0000000000000011',
    'THAT':'0000000000000100'
}

z=[]        #empty list to store the binary values

# Define a dictionary to store the labels and their corresponding addresses
labels = {}
variable={}
lst2=(list(range(16,16384)))
# Open the input file and read the lines
f = open('input.asm', 'r') 
lines = f.readlines()
print(lines)
#White spaces and comments identification and deletion
code=[s.replace('\n','') for s in lines]
code=[s.replace('\t','') for s in code]
code=[s.split("\\")[0] for s in code]
code=[s.split("//")[0] for s in code]
code=[s.replace(" ","")for s in code]
code =[x for x in code if x!='']
#Checking labels and adding into symbols table
print(code)
current_line = 0
label_dict = {}
# Check if this is a label
for line in code:
    if line[0] == '(' :         # Get the label name and store its line number in the label dictionary
        l=line[1:-1]
        label_dict[l] = current_line
    else:
        current_line += 1


# A instruction
for line in code:
    if line[0] == "(":
        pass
    elif line[0] == "@":
        if line[1:].isdigit():
            # This is an A instruction with a constant value
            value = int(line[1:].strip())
            binary_value=f'{value:016b}'          # converting value after @ into a 16-bit binary value
            z.append(binary_value)                # appending the binary value into z[]
        elif line[1:] in symbols.keys():    #checking if it is a symbol in the symbol dictionary
            symbol = line[1:].strip()
            y=symbols[symbol]
            z.append(y) 
        elif line[1:] in label_dict.keys():    #checking if it is a symbol in the symbol dictionary
            label = line[1:].strip()
            y=label_dict[label]
            z.append( f'{y:016b}')
        else:
            if line[1:].strip() not in variable.keys():
                y=lst2.pop(0)
                variable[line[1:]] = y   # Handle symbols that have not yet been defined (i.e. variables)
                binary_value = f'{y:016b}'
                z.append(binary_value)
            else:
                y=variable[line[1:]]
                z.append(f'{y:016b}') 
           
#Cinstruction
    else:
        s=line.split('=')
        c=[]
        if len(s)==1:
            s=line.split(';')
            c=('111'+computation_dictionary[s[0]]+destination_dictionary['null']+jump_dictionary[s[1]])
            z.append(c)
        else:
            t=s[1].split(';')
            if len(t)==2:
                c=('111'+computation_dictionary[t[0]]+destination_dictionary [s[0]]+jump_dictionary[t[1]])
                z.append(c)
            else:
                c='111'+computation_dictionary[t[0]]+destination_dictionary [s[0]]+jump_dictionary['null']
                z.append(c)

print(z)
f2 = open('output.hack', 'w') 
for j in z:
    f2.writelines((j)+"\n")
f.close()
f2.close()

