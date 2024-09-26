import os.path
import pymem
import pymem.process
import pymem.pattern

# TODO: Create Documentation
# TODO: What Kind of Errors from pymem?
# TODO: Clean File
# TODO: Type hinting, some might return None?

def read_memory(_process, _address) -> int:
    pm = pymem.Pymem(_process)
    memory_value = pm.read_longlong(_address)
    return memory_value

def read_memory_int(_process, _address) -> int:
    pm = pymem.Pymem(_process)
    memory_value = pm.read_int(_address)
    return memory_value

def read_memory_short(_process, _address) -> int:
    pm = pymem.Pymem(_process)
    memory_value = pm.read_short(_address)
    return memory_value

def read_memory_float(_process, _address) -> float:
    pm = pymem.Pymem(_process)
    memory_value = pm.read_float(_address)
    return memory_value

def read_memory_bytes(_process, _address, _len) -> bytes:
    pm = pymem.Pymem(_process)
    memory_value = pm.read_bytes(_address, _len)
    return memory_value

def write_memory(_process, _address, _value) -> None: ...

def write_memory_int(_process, _address, _value) -> None: ...

def write_memory_short(_process, _address, _value) -> None: ...

def write_memory_float(_process, _address, _value) -> None:
    pm = pymem.Pymem(_process)
    pm.write_float(_address, _value)

def write_byte(_process, _address, _byte) -> None:
    pm = pymem.Pymem(_process)
    pm.write_bytes(_address, bytes(_byte), len(bytes(_byte)))

def find_pattern_fast(_process, _pattern, _return_multiple = False) -> int | list:
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

def find_pattern_single(_process, _pattern) -> int:
    pm = pymem.Pymem(_process)
    module = pymem.process.module_from_name(pm.process_handle, _process)
    a = pymem.pattern.pattern_scan_module(pm.process_handle, module, _pattern)
    return a

def find_pattern_alt(_process, _pattern) -> int:
    pm = pymem.Pymem(_process)
    a = pymem.pattern.pattern_scan_all(pm.process_handle, _pattern, return_multiple=True)
    return a

def read_cheat_engine_file(_filename) -> int:
    ret_val : int
    if os.path.isfile('place_cheat_table_here/' + _filename):
        with open('place_cheat_table_here/' + _filename, 'r') as file:
            ret_val = int(file.readline())
    return ret_val

if __name__ == "__main__":
    ...