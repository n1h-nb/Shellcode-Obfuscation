import sys   
import argparse  

def get_raw_sc(input_file):
    input_file = input_file
    file_shellcode = b''
    try:
        with open(input_file, 'rb') as shellcode_file:
            file_shellcode = shellcode_file.read()
            file_shellcode = file_shellcode.strip()
        return(file_shellcode)
    except FileNotFoundError:
        exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str,
                        help="Payload to be encrypted.")

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    shellcode = get_raw_sc(args.input)
    # Reverse the shellcode
    reversed = ', '.join(hex(x) for x in shellcode[::-1])

    # Print the length of the shellcode
    print("\n###SHELLCODE_LENGTH###")
    print(str(len(shellcode)))
    # Print the shellcode
    print("\n###SHELLCODE###")
    print(reversed)

    original_shellcode = ""
    for byte in shellcode:
        original_shellcode = original_shellcode + str(hex(byte).zfill(2)) + ", "
    original_shellcode = original_shellcode.rstrip(', ')
    print("\nOriginal shellcode:")
    print(original_shellcode)

if __name__ == '__main__':
    main()
