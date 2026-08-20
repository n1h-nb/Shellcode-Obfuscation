import base64
import sys
import argparse

def get_raw_sc(input_file):
    file_shellcode = b''
    try:
        with open(input_file, 'rb') as shellcode_file:
            file_shellcode = shellcode_file.read()
            file_shellcode = file_shellcode.strip()  
        return file_shellcode
    except FileNotFoundError:
        exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Payload to be encrypted.")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    b64 = ""
    try:
        plaintext = open(args.input, "rb").read()
        # Base64 encode the file contents
        b64 = base64.b64encode(plaintext)
    except FileNotFoundError:
        print("I couldn't find the file you specified: %s" % args.input)
        print("Exiting...\n")
        sys.exit()

    # Print the base64 encoded shellcode string
    print("Base64 encoded shellcode:")
    print(str(b64, "UTF-8"))

    # Retrieve raw shellcode bytes for hex display
    raw_shellcode = get_raw_sc(args.input)
    original_shellcode = ""
    # Convert bytes to zero-padded hex strings separated by commas
    for byte in raw_shellcode:
        original_shellcode += str(hex(byte).zfill(2)) + ", "
    original_shellcode = original_shellcode.rstrip(', ')
    
    # Print original shellcode bytes in hex format
    print("\nOriginal shellcode:")
    print(original_shellcode)

if __name__ == "__main__":
    main()
