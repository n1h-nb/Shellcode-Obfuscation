import random
import argparse
import sys

def gen_word_combinations(dict_file):
    try:
        with open(dict_file) as dictionary:
            words = dictionary.readlines()
    except FileNotFoundError:
        exit("\n\nThe dictionary you specified does not exist! Please specify a valid file path.\nExiting...\n")

    # Randomly select 257 words from the dictionary (fails if fewer than 256)
    try:
        random_words = random.sample(words, 257)
        return random_words
    except ValueError:
        exit("\n\nThe dictionary file you specified does not contain at least 256 words!\nExiting...\n")

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
        return(raw_shellcode)
    
    except FileNotFoundError:
        exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")

def main():
    ### Parse command line arguments for dictionary and input shellcode files
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dictionary", type=str,
                        help="Dictionary file. Defaults to 'dictionary.txt.'")
    parser.add_argument("-i", "--input", type=str,
                        help="File containing raw shellcode.")

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    dict_file = args.dictionary
    input_file = args.input

    '''
        Build a list of 256 random English words for translation table
    '''
    words = gen_word_combinations(dict_file)
    english_array = []
    for i in range(0, 256):
        english_array.append(words.pop(1).strip())

    '''
        Read and format shellcode into comma-separated hex byte strings
    '''
    shellcode = get_shellcode(input_file)
    sc_len = len(shellcode.split(','))

    '''
        Build the translation table string of English words
    '''
    tt_index = 0
    translation_table = ''
    for word in english_array:
        translation_table = translation_table + '"' + word + '",'
        tt_index = tt_index + 1
    translation_table = translation_table.rstrip(', ')
    translation_table = translation_table.replace('XXX', str(tt_index))

    '''
        Translate each byte of shellcode into corresponding English word
    '''
    translated_shellcode_generator = ('"{}"'.format(english_array[int(byte, 16)]) for byte in shellcode.split(','))
    translated_shellcode = ','.join(translated_shellcode_generator)
    translated_shellcode = translated_shellcode.strip(',\'')

    # Print the values
    print("\n###SHELLCODE_LENGTH###")
    print(sc_len)
    print("\n###TRANSLATION_TABLE###")
    print(translation_table)
    print("\n###TRANSLATED_SHELLCODE###")
    print(translated_shellcode)

    # Print the original shellcode string
    print("\nOriginal shellcode:")
    print(shellcode)


if __name__ == '__main__':
    main()
