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
 * @brief Scans a given chunk of data for the given pattern and mask.
 *
 * @param data          The data to scan within for the given pattern.
 * @param baseAddress   The base address of where the scan data is from.
 * @param lpPattern     The pattern to scan for.
 * @param pszMask       The mask to compare against for wildcards.
 * @param offset        The offset to add to the pointer.
 * @param resultUsage   The result offset to use when locating signatures that match multiple functions.
 *
 * @return Pointer of the pattern found, 0 otherwise.
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
    int i;

    // Find the base module for the game
    if (EnumProcessModules(hProcess, hMods, sizeof(hMods), &cbNeeded)) {
        for (i = 0; i < cbNeeded / sizeof(HMODULE); i++) {
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
    DWORD64 moduleBaseAddress;
    DWORD64 moduleSize;

    if (GetModuleInformation(hProcess, hMods[i], &modInfo, sizeof(modInfo))) {
        moduleBaseAddress = (DWORD64)modInfo.lpBaseOfDll;
        moduleSize = modInfo.SizeOfImage;
    }

    if (moduleBaseAddress) {
        std::vector<byte> data(moduleSize);
        SIZE_T bytesRead = 0;
        DWORD oldProtect;

        if (VirtualProtectEx(hProcess, (LPVOID)(baseAddress + offsetAddress), moduleSize, PAGE_EXECUTE_READWRITE, &oldProtect) == 0) {
            std::cout << "Error: " << GetLastError() << std::endl;
            std::cout << "Failed to protect memory" << std::endl;
            return 0;
        }

        if (ReadProcessMemory(hProcess, (LPVOID)(baseAddress + offsetAddress), data.data(), moduleSize, &bytesRead) == 0) {
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
                [&](unsigned char curr, std::pair<unsigned char, bool> currPattern)
            {
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

PYBIND11_MODULE(AOBScanner, m) {
    m.def("AOBScan", &AOBScan);
}