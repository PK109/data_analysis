import re
import pandas as pd
import copy
import difflib

def get_warranty_type(string, default):
    """
    Applies to columns:
    Typ gwarancji
    :param string: text to be verified
    :param default: default value in case of null
    :return: simple value to be categorized
    """
    if string is not None:
        if string == "standardowa":
            return string
        else:
            return "premium"
    else:
        return default

def get_lan_type(string, default):
    """
    Applies to columns:
    Port LAN RJ-45
    :param string: text to be verified
    :param default: default value in case of null
    :return: simplified value to be categorized
    """
    pattern = '(?<=\/)(\d+\s)'
    if string is not None:
        find_result = re.findall(pattern, string)
        if len(find_result) > 0:
            return find_result[0] + " Mbps"
    return default

def simplify_cover(string, default=' '):
    """
    # Applies to column:
    # Materiał obudowy
    :param string: text to be verified
    :param default: default value in case of null
    :return: simplified value to be categorized
    """
    if pd.isna(string):
        string = default

    metal_parts = ['aluminium', 'metal', 'magnez']
    plastic_parts = ['tworzywo sztuczne', 'plastik']
    # check if material name exists in product description
    is_metal = any((material in string) for material in metal_parts)
    is_plastic = any((material in string) for material in plastic_parts)

    if is_metal and is_plastic:
        return "composite"
    elif is_metal:
        return "metal"
    elif is_plastic:
        return "plastic"
    return default

def fun_binarize(string):
    """
    # Applies to columns:
    # Możliwość montażu dodatkowych dysków
    # Czytnik kart pamięci
    # Podświetlana klawiatura
    # Czytnik linii papilarnych
    # Ekran dotykowy
    # Wbudowany mikrofon
    :param string: text to be verified
    :return: boolean value for the dimension
    """
    if string == "nie" or string is None:
        return 0
    else:
        return 1

def is_DDR5(string, default=" "):
    """
    # Applies to columns:
    # Typ pamięci RAM
    :param string: text to be verified
    :param default: default value in case of null
    :return: boolean value for the dimension
    """
    if pd.isna(string):
        string = default

    pattern = 'DDR5'
    match_result = re.search(pattern, string)

    if match_result:
        return 1
    else:
        return 0

def is_mat(string):
    """
    # Applies to columns:
    # Typ matrycy
    :param string: text to be verified
    :return: boolean value for the dimension
    """
    pattern = 'matowa'
    match_result = re.search(pattern, string)

    if match_result:
        return 1
    else:
        return 0

def is_WiFi_ax(string):
    """
    # Applies to columns:
    # Łączność bezprzewodowa
    :param string: text to be verified
    :return: boolean value for the dimension
    """
    pattern = 'ax'
    if string is not None:
        match_result = re.search(pattern, string)
        if match_result:
            return 1
    return 0

def get_first_number(string, default = None):
    """
    # Applies to columns:
    # Zajęte sloty na pamięć RAM
    # Pamięć karty graficznej
    # Gwarancja
    # Liczba rdzeni procesora
    # Pamięć RAM
    # Pojemność baterii/akumulatora
    # Ekran
    # Pamięć podręczna CACHE
    :param string: text to be searched
    :param default: default value in case of null
    :return: integer simplified value
    """
    pattern = '\d+'
    if pd.isna(string) == False:
        find_result = re.findall(pattern, string)
        if len(find_result)> 0:
            return int(find_result[0])
    return default

def get_memory(string):
    """
    # Applies to columns:
    # Szybki dysk SSD
    :param string: text to be searched
    :return: integer simplified value of memory disk in GBs
    """
    pattern_d = '\d+'
    pattern_tb = 'TB'
    multiplier = 1

    if string is not None:
        if re.search(pattern_tb, string):
            multiplier = 1024  # if TB is a unit, multiply result by 1024
        find_result = re.findall(pattern_d, string)
        if len(find_result) > 0:
            return int(find_result[0]) * multiplier
    return 0

def get_camera_data(string, default):
    """
    # Applies to column:
    # Wbudowana kamera
    :param string: text to be verified
    :param default: default value in case of null
    :return: float simplified value resolution in MPx
    """
    if string == "nie" or string is None:
        return 0
    else:
        string = string.replace(",",".")
        pattern = '[0-9.]+'
        find_result = re.findall(pattern, string)
        if len(find_result)> 0:
            return float(find_result[0])
    return default

def get_max_ram(args):
    """
    # Applies to columns:
    # Możliwość rozszerzenia pamięci RAM do
    :param arg[0]: text to be verified
    :param args[1]: default value in case of null
    :return: integer simplified value
    """
    string = args[0]
    default = args[1]
    pattern = '\d+'

    if pd.isna(string) == False:
        find_result = re.findall(pattern, string)
        if len(find_result) > 0:
            return int(find_result[0])

    return default

def get_cpu_frequency(string, default=''):
    """
    # Applies to columns:
    # Częstotliwość taktowania
    :param string: text to be verified
    :param default: default value in case of null
    :return: tupled float values of CPU frequency and boosted frequency in MHz
    """
    if pd.isna(string):
        string = default

    string = string.replace(',', '.')
    pattern = '\d+\.\d+'

    find_result = re.findall(pattern, string)
    if len(find_result) > 0:
        boost = float(find_result[-1]) - float(find_result[0])
        return float(find_result[0]), boost
    else:
        return None, None

def get_unique_interfaces(string):
    """
    :param string: text to be separated
    :return: all types of interfaces listed
    """
    pattern = ',\s|\sx\s\d'
    string_splitted = re.split(pattern, string)
    while '' in string_splitted:
        string_splitted.remove('')
    return string_splitted

def one_hot_encoding_interfaces(string, unique_interfaces):
    """
    # Applies to columns:
    # Złącza
    :param string: text to be separated by interfaces used
    :return: dictionary with keys as interfaces and values as count of interfaces
    """
    records = []
    records_dict = {}
    values = [0 for i in range(len(unique_interfaces))]
    interfaces = copy.deepcopy(dict(zip(unique_interfaces,values)))
    if string is None:
        return interfaces
    for pattern in interfaces:
        pattern = pattern.replace('(','\(').replace(')','\)') # \ prevents treating brackets as a special characters
        pattern = f'({pattern})( x )?(\d)?'
        match = re.findall(pattern, string)
        records.extend(match)
    for record in records:
        if record[1] ==' x ':
            records_dict[record[0]]= int(record[2])
        else:
            records_dict[record[0]]= 1
    interfaces.update(records_dict)
    return interfaces

def get_cpu_benchmarks(cpu, cpu_benchmark):
    """
    # Applies to columns:
    # Model procesora
    :param cpu: cpu name to be identified
    :param cpu_benchmark: dataframe with cpu names and benchmark values
    :return: tuple of the closest cpu name found and its benchmark
    """
    if cpu is None:
        return ['', None]
    #cpu name conditioning - removing unused names and special characters
    pattern = '[^a-zA-Z0-9\s]+'
    cpu = re.sub(pattern,'', cpu)
    pattern = '\d+gen\s' #confusing for intel cpu
    cpu = re.sub(pattern,'', cpu)
    cpu_name = difflib.get_close_matches(cpu, cpu_benchmark['index'])
    if len(cpu_name) > 1:
        cpu_name = cpu_name[0]
        return cpu_name, cpu_benchmark[cpu_benchmark['index'] == cpu_name]['CPU mark'].iloc[0]
    else:
        return '', None

def get_gpu_benchmarks(gpu, gpu_benchmark):
    """
    # Applies to columns:
    # Model karty graficznej
    :param gpu: gpu name to be identified
    :param gpu_benchmark: dataframe with gpu names and benchmark values
    :return: tuple of the closest gpu name found and its benchmark
    """
    if gpu is None:
        return ['', None]
    # gpu name conditioning - removing unused names and special characters
    gpu = gpu.replace(' Graphics', '').replace('NVIDIA ', '').replace('AMD ', '')
    pattern = re.compile('[^a-zA-Z0-9\s]+')
    gpu = pattern.sub('', gpu)
    gpu_name = difflib.get_close_matches(gpu, gpu_benchmark['gpuName'].unique())
    if len(gpu_name) > 1:
        gpu_name = gpu_name[0]
        return gpu_name, int(gpu_benchmark['G3Dmark'][gpu_benchmark['gpuName'] == gpu_name].iloc[0])
    else:
        return '', None
