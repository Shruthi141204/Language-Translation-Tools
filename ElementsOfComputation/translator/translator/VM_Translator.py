import os
# Define the VM translator function
assembly=[]
output_lines= []
def translate_vm(commands):
# Define a dictionary to map VM segment names to their corresponding memory addresses
    segment_map = {
        "argument": "ARG",
        "local": "LCL",
        "static": "16",
        "this": "THIS",
        "that": "THAT",
        "temp": "5",
        "SP": "256"
    }

# call implentation
def call(function_name, num_args):
    global call_counter
    global output_line
    # Push return address label
    return_address = "RETURN_ADDRESS"+function_name  # Use a translator-generated label
    assembly = ["@" + return_address+str(call_counter), "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]

    # Push LCL, ARG, THIS, and THAT of the caller
    segment_pointers = ["LCL", "ARG", "THIS", "THAT"]
    for pointer in segment_pointers:
        assembly.extend(["@" + pointer, "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"])

    # Reposition LCL
    assembly.extend(["@SP", "D=M", "@LCL", "M=D"])
    
    # Reposition ARG
    assembly.extend(["@SP", "D=M", "@5", "D=D-A", "@" + str(num_args), "D=D-A", "@ARG", "M=D"])

    # Transfer control to the called function
    assembly.extend(["@" + function_name, "0;JMP"])

    # Return address label
    assembly.append("(" + return_address+str(call_counter) + ")")
    output_lines.extend(assembly)

    #call counter
    call_counter = call_counter+1
    

name="input"
filename="input.vm"
call_counter = 0
func=""
pointer_map ={"0":"THIS", "1":"THAT"}
    # Open the input file and read the lines
f = open('input.vm', 'r') 
lines = f.readlines()
print(lines)

#White spaces and comments identification and deletion
lines=[s.replace('\n','') for s in lines]
lines=[s.replace('\t','') for s in lines]
lines=[s.split("\\")[0] for s in lines]
lines=[s.split("//")[0] for s in lines]
lines=[s.strip() for s in lines]
lines = [x for x in lines if x != '']
lines=[s.split(" ") for s in lines]
dir_path = os.path.dirname(os.path.realpath(filename))
dir_list = os.listdir(dir_path)
dir_list.remove(filename)

print(dir_path)
print(dir_list)
print(lines)
c=[]
fun=[]
fc=0
for i in lines:
    if (i[0]=="function"):
        fc+=1
    elif (i[0]=="call"):
        fc+=1
        fun.append(i[1].split(".")[0])
        c.append(i[1].split(".")[1])
        
for j in dir_list:
    print(j.split("."))
    if j.split(".")[0] in fun:
        if j.split(".")[1] =="vm":
            f2=open(j,'r')
            sentence=f2.readlines()
            sentence=[s.replace('\n','') for s in sentence]
            sentence=[s.replace('\t','') for s in sentence]
            sentence=[s.split("\\")[0] for s in sentence]
            sentence=[s.split("//")[0] for s in sentence]
            sentence=[s.strip() for s in sentence]
            sentence = [x for x in sentence if x != '']
            sentence=[s.split(" ") for s in sentence]
            print(sentence)
            lines=sentence+lines     

print(fun)
print(c)
print(lines)
print(output_lines)

output_lines.append("@256"),
output_lines.append("D=A"),
output_lines.append("@0"),
output_lines.append("M=D")

if (fc>1):
    print("Calling sys init \n\n\n\n\n")
    call("Sys.init",0)


#push/pop for all the stacks
def write_push(segment, index):
    global name
    global output_line
    global pointer_map
    global func
    """
    Writes the assembly lines that implements the "push segment index" command in the VM language.
    """
# Determine the memory segment to push from.
    if segment == "constant":
        assembly = [
            "@"+index,
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif segment == "local":
        assembly = [
            "@LCL",
            "D=M",
            "@"+index,
            "A=D+A",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif segment == "argument":
        assembly = [
            "@ARG",
            "D=M",
            f"@{index}",
            "A=D+A",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif segment == "this":
        assembly = [
            "@THIS",
            "D=M",
            f"@{index}",
            "A=D+A",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif segment == "that":
        assembly = [
            "@THAT",
            "D=M",
            f"@{index}",
            "A=D+A",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif segment == "pointer":
        assembly = [
            "@"+pointer_map[index],
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
            
        ]
    elif segment == "temp":
        assembly = [
           "@"+index,
           "D=A",
           "@5",
           "A=D+A",
           "D=M",
           "@SP",
           "A=M",
           "M=D",
           "@SP",
           "M=M+1"
           
        ]
    elif segment == "static":
        assembly = [
            "@"+func+"."+index,
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
          ]
        
    else:
        raise ValueError(f"Invalid segment: {segment}")
    output_lines.extend(assembly)


def write_pop(segment, index):
    global output_lines
    global pointer_map
    global name
    global func
    """
    Writes the assembly code that implements the "pop segment index" command in the VM language.
    """
# Determine the memory segment to pop to.
    if segment == "local":
        assembly = [
            "@LCL",
            "D=M",
            f"@{index}",
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
    elif segment == "argument":
        assembly = [
            "@ARG",
            "D=M",
            f"@{index}",
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
    elif segment == "this":
        assembly = [
            "@THIS",
            "D=M",
            f"@{index}",
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
    elif segment == "that":
        assembly = [
            "@THAT",
            "D=M",
            f"@{index}",
            "D=D+A",
            "@R13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
    elif segment == "pointer":
        assembly = [
            "@SP",
            "AM=M-1",
            "D=M",
            "@"+pointer_map[index],
            "M=D"
        ]
    elif segment == "temp":
        assembly = [
           "@"+index,
           "D=A",
           "@5",
           "D=D+A",
           "@13",
           "M=D",
           "@SP",
           "M=M-1",
           "A=M",
           "D=M",
           "@13",
           "A=M",
           "M=D"
        ]
    elif segment == "static":
        assembly = [
            "@"+func+"."+index,
            "D=A",
            "@13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D"
        ]
    else:
        raise ValueError(f"Invalid segment: {segment}")
    output_lines.extend(assembly)
    


#If-goto and goto
def if_goto(label):
    global output_lines
    assembly = [
        "@SP",
        "AM=M-1",
        "D=M",
        "@"+label,
        "D;JNE"
       ] 
    output_lines.extend(assembly)
     

def goto(label):
    global output_lines
    assembly = [
        "@"+label,
        "0;JMP"
    ]
    output_lines.extend(assembly)

def label(label):
    global output_lines
    output_lines.append("("+label+")")
    
    
#functions implementation:
def functions(f_name,n_vars):
    global output_lines
    inst=["("+f_name+")"]
    for i in range(int(n_vars)):
        inst.extend([ 
            "@SP",         # Load the stack pointer
            "A=M",         # Set A to the address pointed by SP
            "M=0",         # Store the counter value at the address pointed by SP
            "@SP",         # Load the stack pointer
            "M=M+1"        # Increment the stack pointer
        ])
    output_lines.extend(inst)
    


# Define a function to generate assembly code for arithmetic operations
def arithmetic(command):
    global output_lines
    if command == "add":
        output_lines.append("@SP")
        output_lines.append("AM=M-1")
        output_lines.append("D=M")
        output_lines.append("A=A-1")
        output_lines.append("M=D+M")
    elif command == "sub":
        output_lines.append("@SP")
        output_lines.append("AM=M-1")
        output_lines.append("D=M")
        output_lines.append("A=A-1")
        output_lines.append("M=M-D")
    elif command == "neg":
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=-M")
    elif command == "eq":  
        output_lines.append("@SP")
        output_lines.append("AM=M-1")
        output_lines.append("D=M")
        output_lines.append("A=A-1")
        output_lines.append("D=M-D")
        output_lines.append("@EQ_TRUE")
        output_lines.append("D;JEQ")
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=0")
        output_lines.append("@EQ_END")
        output_lines.append("0;JMP")
        output_lines.append("(EQ_TRUE)")
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=-1")
        output_lines.append("(EQ_END)")
    elif command == "gt":
        output_lines.append("@SP")
        output_lines.append("AM=M-1")
        output_lines.append("D=M")
        output_lines.append("A=A-1")
        output_lines.append("D=M-D")
        output_lines.append("@GT_TRUE")
        output_lines.append("D;JGT")
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=0")
        output_lines.append("@GT_END")
        output_lines.append("0;JMP")
        output_lines.append("(GT_TRUE)")
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=-1")
        output_lines.append("(GT_END)")
    elif command == "lt":
        output_lines.append("@SP")
        output_lines.append("AM=M-1")
        output_lines.append("D=M")
        output_lines.append("A=A-1")
        output_lines.append("D=M-D")
        output_lines.append("@LT_TRUE")
        output_lines.append("D;JLT")
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=0")
        output_lines.append("@LT_END")
        output_lines.append("0;JMP")
        output_lines.append("(LT_TRUE)")
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=-1")
        output_lines.append("(LT_END)")
    elif command == "and":
        output_lines.append("@SP")
        output_lines.append("AM=M-1")
        output_lines.append("D=M")
        output_lines.append("A=A-1")
        output_lines.append("M=D&M")     
    elif command == "or":
        output_lines.append("@SP")
        output_lines.append("AM=M-1")
        output_lines.append("D=M")
        output_lines.append("A=A-1")
        output_lines.append("M=D|M")       
    elif command == "not":
        output_lines.append("@SP")
        output_lines.append("A=M-1")
        output_lines.append("M=!M")
    else:
        return ""
    print(output_lines)



def write_return():
    global output_lines
    """
    Writes the assembly lines that implements the "return" command in the VM language.
    """
# Store the current frame pointer (LCL) in a temporary variable.
# This will be used later to restore the caller's state.
    assembly = [
        "// return",
        "@LCL",
        "D=M",
        "@R13",
        "M=D"
    ]
    
    
# Store the return address (the value at the top of the caller's stack) in a temporary variable.
    assembly += [
# Get the return address (stored at LCL - 5) and store it in R14.
        "@5",
        "A=D-A",
        "D=M",
        "@R14",
        "M=D"
    ]
    
    
# Move the return value (the value at the top of the callee's stack) to the caller's stack.
    assembly += [
# Get the return value (stored at the top of the callee's stack) and store it in ARG 0.
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@ARG",
        "A=M",
        "M=D"
    ]
    
    
# Restore the caller's stack pointer.
    assembly += [
# Set SP to ARG + 1
        "@ARG",
        "D=M",
        "@SP",
        "M=D+1"
    ]
    
    
# Restore the caller's state by restoring the caller's segment pointers.
    assembly += [
# Restore THAT pointer (THAT = *(frame - 1))
        "@R13",
        "AM=M-1",
        "D=M",
        "@THAT",
        "M=D",

# Restore THIS pointer (THIS = *(frame - 2))
        "@R13",
        "AM=M-1",
        "D=M",
        "@THIS",
        "M=D",

# Restore ARG pointer (ARG = *(frame - 3))
        "@R13",
        "AM=M-1",
        "D=M",
        "@ARG",
        "M=D",

# Restore LCL pointer (LCL = *(frame - 4))
        "@R13",
        "AM=M-1",
        "D=M",
        "@LCL",
        "M=D",
        ]
    
# Jump to the return address.
    assembly += [
# Jump to the return address (stored in R14).
        "@R14",
        "A=M",
        "0;JMP"
    ]
    output_lines.extend(assembly)
    
for line in lines:
    segments = line
    print(segments)
    if len(segments) == 1:
        if segments[0] in ["add", "sub", "neg","eq", "gt", "lt", "and", "or", "not"]:
            output_lines.append(arithmetic(segments[0]))
        elif segments[0] == "return":
            write_return()
        else:
            output_lines.append(" ".join(segments))
    elif len(segments)==3:
        print(segments)
        if segments[0] == "push":
            write_push(segments[1],segments[2])
        elif segments[0] == "pop":
            write_pop(segments[1],segments[2])
        elif  segments[0] == "call":
            call(segments[1],segments[2])
        elif segments[0] == "function":
            func=segments[1].split(".")[0]
            functions(segments[1],segments[2])
    elif len(segments) == 2:
        if segments[0] == "if-goto":
             if_goto(segments[1])
        elif segments[0] == "goto":
             goto(segments[1])
        elif segments[0] == "label":
             label(segments[1])

output_lines.append("(End)")
output_lines.append("@End")
output_lines.append("0;JMP")
print(output_lines)



            
print(output_lines)
f2 = open('input.asm', 'w') 
for j in output_lines:
    if j== None:
        pass
    else:
        f2.writelines((j)+"\n")
f.close()
f2.close()

