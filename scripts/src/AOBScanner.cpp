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

int readInteger(int pid, intptr_t address) {
    int ret = 0;
    std::vector bytes = readBytes(pid, address, sizeof(int));

    unsigned char buffer[sizeof(int)];
    std::copy(bytes.begin(), bytes.end(), buffer);
    memcpy(&ret, &buffer, sizeof(int));

    return ret;
}

bool writeInteger(int pid, intptr_t address, const int num) {
    int localNum = num;
    unsigned char buffer[sizeof(int)];
    memcpy(&buffer, &localNum, sizeof(int));

    std::vector<unsigned char> ret(buffer, buffer + sizeof(int));

    return writeBytes(pid, address, sizeof(int), ret);
}

float readFloat(int pid, intptr_t address) {
    float ret = 0;
    std::vector bytes = readBytes(pid, address, sizeof(float));

    unsigned char buffer[sizeof(float)];
    std::copy(bytes.begin(), bytes.end(), buffer);
    memcpy(&ret, &buffer, sizeof(float));

    return ret;
}

bool writeFloat(int pid, intptr_t address, const float num) {
    float localNum = num;
    unsigned char buffer[sizeof(float)];
    memcpy(&buffer, &localNum, sizeof(float));

    std::vector<unsigned char> ret(buffer, buffer + sizeof(float));

    return writeBytes(pid, address, sizeof(float), ret);
}

double readDouble(int pid, intptr_t address) {
    double ret = 0;
    std::vector bytes = readBytes(pid, address, sizeof(double));

    unsigned char buffer[sizeof(double)];
    std::copy(bytes.begin(), bytes.end(), buffer);
    memcpy(&ret, &buffer, sizeof(double));

    return ret;
}

bool writeDouble(int pid, intptr_t address, const double num) {
    double localNum = num;
    unsigned char buffer[sizeof(double)];
    memcpy(&buffer, &localNum, sizeof(double));

    std::vector<unsigned char> ret(buffer, buffer + sizeof(double));

    return writeBytes(pid, address, sizeof(double), ret);
}

long readLong(int pid, intptr_t address) {
    long ret = 0;
    std::vector bytes = readBytes(pid, address, sizeof(long));

    unsigned char buffer[sizeof(long)];
    std::copy(bytes.begin(), bytes.end(), buffer);
    memcpy(&ret, &buffer, sizeof(long));

    return ret;
}

bool writeLong(int pid, intptr_t address, const long num) {
    long localNum = num;
    unsigned char buffer[sizeof(long)];
    memcpy(&buffer, &localNum, sizeof(long));

    std::vector<unsigned char> ret(buffer, buffer + sizeof(long));

    return writeBytes(pid, address, sizeof(int), ret);
}

long long readLongLong(int pid, intptr_t address) {
    long long ret = 0;
    std::vector bytes = readBytes(pid, address, sizeof(long long));

    unsigned char buffer[sizeof(long long)];
    std::copy(bytes.begin(), bytes.end(), buffer);
    memcpy(&ret, &buffer, sizeof(long long));

    return ret;
}

bool writeLongLong(int pid, intptr_t address, const long long num) {
    long long localNum = num;
    unsigned char buffer[sizeof(long long)];
    memcpy(&buffer, &localNum, sizeof(long long));

    std::vector<unsigned char> ret(buffer, buffer + sizeof(long long));

    return writeBytes(pid, address, sizeof(long long), ret);
}

short readShort(int pid, intptr_t address) {
    short ret = 0;
    std::vector bytes = readBytes(pid, address, sizeof(short));

    unsigned char buffer[sizeof(short)];
    std::copy(bytes.begin(), bytes.end(), buffer);
    memcpy(&ret, &buffer, sizeof(short));

    return ret;
}

bool writeShort(int pid, intptr_t address, const short num) {
    short localNum = num;
    unsigned char buffer[sizeof(short)];
    memcpy(&buffer, &localNum, sizeof(short));

    std::vector<unsigned char> ret(buffer, buffer + sizeof(short));

    return writeBytes(pid, address, sizeof(short), ret);
}

PYBIND11_MODULE(AOBScanner, m) {
    m.def("AOBScan", &AOBScan);
    m.def("readBytes", &readBytes);
    m.def("writeBytes", &writeBytes);
    m.def("readInteger", &readInteger);
    m.def("writeInteger", &writeInteger);
    m.def("readFloat", &readFloat);
    m.def("writeFloat", &writeFloat);
    m.def("readDouble", &readDouble);
    m.def("writeDouble", &writeDouble);
    m.def("readLong", &readLong);
    m.def("writeLong", &writeLong);
    m.def("readLongLong", &readLongLong);
    m.def("writeLongLong", &writeLongLong);
    m.def("readShort", &readShort);
    m.def("writeShort", &writeShort);
}