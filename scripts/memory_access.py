import os
import ctypes
import win32gui
import win32.win32process
import pymem
import pymem.process
import pymem.pattern
import sys

# TODO: Create Documentation
# TODO: What Kind of Errors from pymem?
# TODO: Clean File

def read_memory(_process, _address):
    pm = pymem.Pymem(_process)
    memory_value = pm.read_longlong(_address)
    return memory_value

def read_memory_i(_process, _address):
    pm = pymem.Pymem(_process)
    memory_value = pm.read_int(_address)
    return memory_value

def read_memory_s(_process, _address):
    pm = pymem.Pymem(_process)
    memory_value = pm.read_short(_address)
    return memory_value

def read_memory_bytes(_process, _address, _len):
    pm = pymem.Pymem(_process)
    memory_value = pm.read_bytes(_address, _len)
    return memory_value

def base_pointer(_process):
    pm = pymem.Pymem(_process)
    return pm.base_address

def write_byte(_process, _address, _byte):
    pm = pymem.Pymem(_process)
    pm.write_bytes(_address, bytes(_byte), len(bytes(_byte)))

def find_pattern_fast(_process, _pattern, _return_multiple = False):
    pm = pymem.Pymem(_process)
    if _return_multiple:
        modules = list(pm.list_modules())
        addresses = []
        for module in modules:
            a = pymem.pattern.pattern_scan_module(pm.process_handle, module, _pattern)
            if a:
                addresses.append(a)
        return addresses
    else:
        module = pymem.process.module_from_name(pm.process_handle, _process)
        a = pymem.pattern.pattern_scan_module(pm.process_handle, module, _pattern)
        return a

def find_pattern_single(_process, _pattern):
    pm = pymem.Pymem(_process)
    module = pymem.process.module_from_name(pm.process_handle, _process)
    a = pymem.pattern.pattern_scan_module(pm.process_handle, module, _pattern)
    return a

def find_pattern_alt(_process, _pattern):
    pm = pymem.Pymem(_process)
    a = pymem.pattern.pattern_scan_all(pm.process_handle, _pattern, return_multiple=True)
    return a

if __name__ == "__main__":
    ...