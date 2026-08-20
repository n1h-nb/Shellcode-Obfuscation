import random         
import sys            
import argparse       

def getShellcode(input_file):
    file_shellcode = b''  
    try:
        with open(input_file, 'rb') as shellcode_file:
            file_shellcode = shellcode_file.read()
            file_shellcode = file_shellcode.strip()     
            binary_code = ''                            
            sc_array = []                               

            for byte in file_shellcode:
                binary_code += "\\x" + hex(byte)[2:].zfill(2)
            raw_shellcode = "0" + ",0".join(binary_code.split("\\")[1:])

        for byte in raw_shellcode.split(','):
            sc_array.append(byte)
        return sc_array  

    except FileNotFoundError:
        sys.exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")

def generateJigsaw(shellcode):
    sc_len = len(shellcode)                     # Get shellcode length
    raw_positions = list(range(0, sc_len))      
    random.shuffle(raw_positions)               # Shuffle positions for obfuscation

    jigsaw = []                                # List to store shuffled shellcode
    # Insert shellcode bytes in shuffled order
    for position in raw_positions:
        jigsaw.append(shellcode[position])

    # Create comma-separated string of shuffled shellcode bytes
    jigsaw_array = ', '.join(str(byte) for byte in jigsaw)
    # Create comma-separated string of positions
    position_array = ', '.join(str(x) for x in raw_positions)
    return jigsaw_array, position_array         # Return shuffled data and positions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str,
                        help="File containing raw shellcode.")

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    if args.input:
        input_file = args.input
    else:
        sys.exit("\nNo input file provided. Please specify the path to the shellcode file.\nExiting...\n")

    shellcode = getShellcode(input_file)          # Read and format shellcode
    jigsaw, positions = generateJigsaw(shellcode) # Shuffle shellcode and get positions

    # Print values
    print("\n###SHELLCODE_LENGTH###:", len(shellcode))
    print("\n###JIGSAW###:", jigsaw)
    print("\n###POSITIONS###:", positions)
    print("\nOriginal shellcode:")                # Print original shellcode
    print(*(x for x in shellcode))

if __name__ == "__main__":
    main()
