import argparse		
import sys		

def get_shellcode(input_file):
    file_shellcode = b''
    try:
        with open(input_file, 'rb') as shellcode_file:
            file_shellcode = shellcode_file.read()
            file_shellcode = file_shellcode.strip()
            
            binary_code = ''
            for byte in file_shellcode:
                binary_code += "\\x" + hex(byte)[2:].zfill(2)
         
            raw_shellcode = "0" + ",0".join(binary_code.split("\\")[1:])
        return (file_shellcode, raw_shellcode)
    except FileNotFoundError:
        exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")

def caesar(sc_list):
    sc = []

    # For each byte, add 13 with wraparound at 255
    for x in sc_list:
        if (int(x) + 13) > 255:
            # Wrap around by subtracting 256 if value exceeds 255
            sc.append("0x" + hex(x + 13 - 256)[2:].zfill(2))
        else:
            # Otherwise, just add 13
            sc.append("0x" + hex(x + 13)[2:].zfill(2))
    return sc

def main():
    # Argument parser to accept input shellcode file path
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str)

    # If no arguments, show help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    # Read shellcode from input file provided
    shellcode, raw_shellcode = get_shellcode(input_file)

    # Apply Caesar cipher to shellcode bytes
    caesar_sc = caesar(shellcode)

    # Print the encrypted shellcode length
    print("###SC_LENGTH###")
    print(len(caesar_sc))

    # Print the encrypted shellcode bytes as comma-separated values
    print("###CAESAR###")
    print(", ".join(caesar_sc))

    # Print original shellcode for verification
    print("\nThe original shellcode is:\n")
    print(raw_shellcode)

if __name__ == '__main__':
    main()
