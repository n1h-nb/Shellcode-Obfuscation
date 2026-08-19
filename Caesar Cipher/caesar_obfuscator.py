import argparse		# Import argparse for command-line argument parsing
import sys		# Import sys for system-specific parameters and functions

def get_shellcode(input_file):
    # Initialize an empty byte string to hold shellcode
    file_shellcode = b''
    try:
        # Open the input file in binary read mode
        with open(input_file, 'rb') as shellcode_file:
            # Read all bytes from the file
            file_shellcode = shellcode_file.read()
            # Remove leading/trailing whitespace bytes
            file_shellcode = file_shellcode.strip()
            
            binary_code = ''
            # Convert each byte to an escaped hex string (e.g., \x90)
            for byte in file_shellcode:
                binary_code += "\\x" + hex(byte)[2:].zfill(2)
            
            # Format for printing: 0xXX,0xXX,... without leading backslashes
            raw_shellcode = "0" + ",0".join(binary_code.split("\\")[1:])

        # Return raw bytes and printable hex string
        return (file_shellcode, raw_shellcode)

    except FileNotFoundError:
        # Exit if specified input file does not exist
        exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")

def caesar(sc_list):
    # Initialize list for Caesar-shifted shellcode bytes
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

# Execute main function when script is run
if __name__ == '__main__':
    main()
