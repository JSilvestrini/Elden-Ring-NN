#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <windows.h>
#include <tlhelp32.h>
#include <vector>
#include <memoryapi.h>
#include <psapi.h>
#include <debugapi.h>

/**
 * @brief               Scans a given chunk of data for the given pattern and mask.
 *
 * @param data          The data to scan within for the given pattern.
 * @param baseAddress   The base address of where the scan data is from.
 * @param lpPattern     The pattern to scan for.
 * @param pszMask       The mask to compare against for wildcards.
 * @param offset        The offset to add to the pointer.
 * @param resultUsage   The result offset to use when locating signatures that match multiple functions.
 *
 * @return              Pointer of the pattern found, 0 otherwise.
 */
static intptr_t AOBScan(int pid, const char* moduleName, intptr_t processAddress, const std::vector<uint8_t>& lpPattern, const char* pszMask, intptr_t offset, intptr_t resultUsage) {
    DWORD processID = (DWORD)pid;
    DWORD64 baseAddress = (DWORD64)processAddress;
    intptr_t offsetAddress = processAddress - baseAddress;
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, false, processID);

    // Ensures that Elden Ring is running
    if (!hProcess) {
        std::cout << "Failed to open process" << std::endl;
        return 0;
    }

    HMODULE hMods[1024];
    DWORD cbNeeded;
    int i = 0;

    // Find the base module for the game
    if (EnumProcessModules(hProcess, hMods, sizeof(hMods), &cbNeeded)) {
        for (i; i < cbNeeded / sizeof(HMODULE); i++) {
            WCHAR szModName[MAX_PATH];
            if (GetModuleFileNameExW(hProcess, hMods[i], szModName, MAX_PATH)) {
                // Convert the wide character string to a narrow character string if needed
                wchar_t wideModuleName[MAX_PATH];
                MultiByteToWideChar(CP_ACP, 0, moduleName, -1, wideModuleName, MAX_PATH);

                wchar_t* lastSlash = wcsrchr(szModName, L'\\');

                if (lastSlash != nullptr) {
                    // Compare the filename part
                    if (wcscmp(lastSlash + 1, wideModuleName) == 0) {
                        //std::cout << "Found module " << moduleName << std::endl;
                        break;
                    }
                }
            }
        }
    }

    // Get the size and base address of the module (the base address is not used in this case)
    MODULEINFO modInfo = {0};
    DWORD64 moduleBaseAddress = NULL;
    DWORD64 moduleSize = NULL;

    if (GetModuleInformation(hProcess, hMods[i], &modInfo, sizeof(modInfo))) {
        moduleBaseAddress = (DWORD64)modInfo.lpBaseOfDll;
        moduleSize = modInfo.SizeOfImage;
    }

    if (moduleBaseAddress != NULL) {
        std::vector<byte> data(moduleSize);
        SIZE_T bytesRead = 0;
        DWORD oldProtect;

        if (VirtualProtectEx(hProcess, (LPVOID)(baseAddress + offsetAddress), moduleSize, PAGE_EXECUTE_READWRITE, &oldProtect) == 0) {
            std::cout << "Error: " << GetLastError() << std::endl;
            std::cout << "Failed to protect memory" << std::endl;
            return 0;
        }

        if (ReadProcessMemory(hProcess, (LPCVOID)(baseAddress + offsetAddress), data.data(), moduleSize, &bytesRead) == 0) {
            std::cout << "Error: " << GetLastError() << std::endl;
            std::cout << "Failed to read process memory" << std::endl;
            return 0;
        }

        //std::cout << "Read " << bytesRead << " bytes" << std::endl;

        // Build vectored pattern..
        std::vector<std::pair<unsigned char, bool>> pattern;
        for (size_t x = 0, y = strlen(pszMask); x < y; x++) {
            pattern.push_back(std::make_pair(lpPattern[x], pszMask[x] == 'x'));
        }

        auto scanStart = data.begin();
        auto resultCnt = 0;

        while (true) {
            // Search for the pattern..
            auto ret = std::search(scanStart, data.end(), pattern.begin(), pattern.end(),
                [&](unsigned char curr, std::pair<unsigned char, bool> currPattern) {
                return (!currPattern.second) || curr == currPattern.first;
            });

            // Did we find a match..
            if (ret != data.end()) {
                // If we hit the usage count, return the result..
                if (resultCnt == resultUsage || resultUsage == 0) {
                    VirtualProtectEx(hProcess, (LPVOID)(baseAddress + offsetAddress), moduleSize, oldProtect, &oldProtect);
                    CloseHandle(hProcess);
                    return (std::distance(data.begin(), ret) + processAddress) + offset;
                }

                // Increment the found count and scan again..
                ++resultCnt;
                scanStart = ++ret;
            }
            else
                break;
        }
    }

    std::cout << "Failed to find pattern" << std::endl;
    return 0;
}

/*
When reading, just read memory
When writing, VirtualProtectEx, then write,
    Then restore old Protections
*/
/**
 * @brief           Reads n Bytes from a Process
 *
 * @param pid       Process ID of the Process
 * @param address   Address to Read from
 * @param n         Number of Bytes to Read
 * 
 * @return          Vector Containing the Bytes
 */
std::vector<unsigned char> readBytes(int pid, intptr_t address, int n) {
    DWORD processID = (DWORD)pid;
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, false, processID);

    // Ensures that Elden Ring is running
    if (!hProcess) {
        std::cout << "Failed to open process" << std::endl;
        return std::vector<unsigned char>();
    }

    unsigned char* buffer = new unsigned char[n];
    SIZE_T bytesRead;

    ReadProcessMemory(hProcess, (LPCVOID)(address), buffer, n, &bytesRead);

    std::vector<unsigned char> ret(buffer, buffer + n);

    delete buffer;
    CloseHandle(hProcess);

    return ret;
}

bool writeBytes(int pid, intptr_t address, int n, const std::vector<unsigned char>& bytes) {
    DWORD processID = (DWORD)pid;
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, false, processID);

    // Ensures that Elden Ring is running
    if (!hProcess) {
        std::cout << "Failed to open process" << std::endl;
        return false;
    }

    unsigned char* buffer = new unsigned char[n];
    std::copy(bytes.begin(), bytes.end(), buffer);
    SIZE_T bytesWritten;

    WriteProcessMemory(hProcess, (LPVOID)(address), buffer, n, &bytesWritten);

    delete buffer;
    return bytesWritten == n;
}

//int readInteger(int pid, int address) {}
//bool writeInteger(int pid, int address, const int num) {}

//float readFloat(int pid, int address) {}
//bool writeFloat(int pid, int address, const float num) {}

//double readDouble(int pid, int address) {}
//bool writeDouble(int pid, int address, const double num) {}

//long readLong(int pid, int address) {}
//bool writeLong(int pid, int address, const long num) {}

//long long readLongLong(int pid, int address) {}
//bool writeLongLong(int pid, int address, const long long num) {}

//short readShort(int pid, int address) {}
//bool writeShort(int pid, int address, const short num) {}

PYBIND11_MODULE(AOBScanner, m) {
    m.def("AOBScan", &AOBScan);
    m.def("readBytes", &readBytes);
    m.def("writeBytes", &writeBytes);
}