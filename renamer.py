import os
from sys import exit as abort
os.system("cls")

"""
    TODO:
    gui
    stats
"""

"""
Available modes:
    1 - Prefix + Index
        Required:
            prefix
        Optional:
            sort_by_created_date
            sort_by_modified_date
            
    2 - Original Name + Index
        Required:
            separators
        Optional:
            sort_by_created_date
            sort_by_modified_date
            
    3 - Prefix + Original Name
        Required:
            prefix
        Optional:
            sort_by_created_date
            sort_by_modified_date
            trim_all_prefixes (Recommended, but read the comment first)
            
    4 - Prefix + Original Name + Index
        Required:
            prefix
            separators
        Optional:
            sort_by_created_date
            sort_by_modified_date
            trim_all_prefixes (Recommended, but read the comment first)
            
    5 - Custom Name + Index
        Required:
            custom_name
            separators
        Optional:
            sort_by_created_date
            sort_by_modified_date
            
    6 - Prefix + Custom Name + Index
        Required:
            prefix
            custom_name
            separators
        Optional:
            sort_by_created_date
            sort_by_modified_date
            trim_all_prefixes (Recommended, but read the comment first)
"""

MODE: int = 1

# set a custom path to a directory or use the script only in the current folder
# make sure the r is before the first string
PATH: str = r''
USE_CURRENT_WORKING_DIRECTORY: bool = False

PREFIX: str = 'd'

CUSTOM_NAME: str = 'pic'

SORT_BY_CREATED_DATE: bool = False
SORT_BY_MODIFIED_DATE: bool = False

ALLOWED_FORMATS: list[str] = [ '.mp4', '.mov', '.avi', '.png', '.jpg' ]

# will remove every index that follows this template, until reaches <other>:
# <other><separator><number>[...]<separator><number>
SEPARATORS: list[str] = [ ' ', '_' ]

# will remove every prefix that follows this template:
# <any>_[...]<any>_
# so make sure your name does not contain any underscores _
# setting this to False means only 1 prefix will be removed
# if you wish to leave them untouched, choose a mode without 'prefix' 
TRIM_ALL_PREFIXES: bool = True

#######################################################################################

REVISION = [
    '17/I/2024',
    'v1.3'
]

errors = [param for param, condition in zip(
    [
        'Parametre [MODE] must be a string',
        'Parametre [PATH] must be a string',
        'Parametre [USE_CURRENT_WORKING_DIRECTORY] must be a bool', #must be before 2nd path check
        'Parametre [PATH] must not be empty when [USE_CURRENT_WORKING_DIRECTORY] is disabled',
        'Parametre [PATH] must be empty when [USE_CURRENT_WORKING_DIRECTORY] is enabled, choose either of them',
        'Parametre [PREFIX] must be a string',
        'Parametre [PREFIX] must not be empty',
        'Parametre [CUSTOM_NAME] must be a string',
        'Parametre [CUSTOM_NAME] must not be empty',
        'Parametre [SORT_BY_CREATED_DATE] must be a bool',
        'Parametre [SORT_BY_MODIFIED_DATE] must be a bool',
        'Parametres [SORT_BY_CREATED_DATE] and [SORT_BY_MODIFIED_DATE] must not be enabled at the same time',
        'Parametre [ALLOWED_FORMATS] must be a list',
        'Parametre [ALLOWED_FORMATS] must not be empty',
        'Parametre [ALLOWED_FORMATS] must contain only strings',
        'Parametre [SEPARATORS] must be a list',
        'Parametre [SEPARATORS] must not be empty',
        'Parametre [SEPARATORS] must contain only strings',
        'Parametre [TRIM_ALL_PREFIXES] must be a bool'
    ],
    [
        isinstance(MODE, int),
        isinstance(PATH, str),
        isinstance(USE_CURRENT_WORKING_DIRECTORY, bool),
        not (PATH == '' and not USE_CURRENT_WORKING_DIRECTORY),
        not (PATH != '' and USE_CURRENT_WORKING_DIRECTORY),
        isinstance(PREFIX, str),
        PREFIX != '',
        isinstance(CUSTOM_NAME, str),
        CUSTOM_NAME != '',
        isinstance(SORT_BY_CREATED_DATE, bool),
        isinstance(SORT_BY_MODIFIED_DATE, bool),
        not (SORT_BY_CREATED_DATE and SORT_BY_MODIFIED_DATE),
        isinstance(ALLOWED_FORMATS, list),
        len(ALLOWED_FORMATS) > 0,
        all(isinstance(elem, str) for elem in ALLOWED_FORMATS),
        isinstance(SEPARATORS, list),
        len(SEPARATORS) > 0,
        all(isinstance(elem, str) for elem in SEPARATORS),
        isinstance(TRIM_ALL_PREFIXES, bool)
    ]
) if not condition]

if errors:
    for error in errors:
        print(error)
    abort('Process aborted due to invalid config')
else:
    if SORT_BY_CREATED_DATE == True:
        sort_mode = 1
    elif SORT_BY_MODIFIED_DATE == True:
        sort_mode = 2
    else:
        sort_mode = 0
        
    if USE_CURRENT_WORKING_DIRECTORY:
        PATH = os.getcwd()
    else:
        if not os.path.exists(PATH):
            abort('Process aborted, PATH does not exist')

    PATH += '\\'

def sort_by_x_date() -> list:
    files = [file for file in os.listdir(PATH) for ext in ALLOWED_FORMATS if ext in file]
    if sort_mode > 0:
        if sort_mode == 1:
            files = [ PATH + file for file in files ]
            files.sort(key=os.path.getctime)
            files = [file.replace(PATH, '') for file in files]
        elif sort_mode == 2:
            files = [ PATH + file for file in files ]
            files.sort(key=os.path.getmtime)
            files = [file.replace(PATH, '') for file in files]
            
        return files
    elif sort_mode == 0:
        return files

def trimmer(file_list:list=[], trim_idx:bool=True, trim_pre:bool=True) -> list:
    done, nums = [], [ str(num) for num in range(10) ]
    for file in file_list:
        name, _ = os.path.splitext(file)
        name = name[::-1]
        
        if trim_idx and (name[0] in nums) or (name[0] in SEPARATORS):
            to_cut, last_separator_idx = 0, 0
            last_char = None
            for idx, char in enumerate(name):
                if char in nums:
                    to_cut += 1
                    last_char = int
                elif char in SEPARATORS:
                    to_cut += 1
                    last_char = str
                    last_separator_idx = idx
                else:
                    if last_char is str:
                        name = name[to_cut:]
                        break
                    elif last_char is int and last_separator_idx > 0:
                        name = name[last_separator_idx+1:]
                        break
                    else:
                        break
        
        name = name[::-1]
        
        if trim_pre:
            for _ in range(1):
                pos = name.find('_')
                if pos != -1:
                    name = name[pos+1:]
                while TRIM_ALL_PREFIXES:
                    pos = name.find('_')
                    if pos != -1:
                        name = name[pos+1:]
                    else:
                        break

        done.append(name)
    
    unique = {}
    for name in done:
        if unique.get(name) is None:
            unique[name] = 1

    return done, unique

def trim_temp():
    for file in os.listdir(PATH):
        name = file.replace('temp_', '')
        os.rename(PATH + file, PATH + name)

if MODE == 1:
    files = sort_by_x_date()
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        new_name = f'temp_{PREFIX}_{idx+1}{ext.lower()}'
        os.rename(PATH + file, PATH + new_name)

elif MODE == 2:
    files = sort_by_x_date()
    names, unique = trimmer(files, trim_pre=False)
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        val = unique.get(names[idx])
        unique[names[idx]] += 1
        new_name = f'temp_{names[idx]} {val}{ext.lower()}'
        os.rename(PATH + file, PATH + new_name)

elif MODE == 3:
    files = sort_by_x_date()
    names, unique = trimmer(files, False)
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        new_name = f'temp_{PREFIX}_{names[idx]}{ext.lower()}'
        os.rename(PATH + file, PATH + new_name)

elif MODE == 4:
    files = sort_by_x_date()
    names, unique = trimmer(files)
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        val = unique.get(names[idx])
        unique[names[idx]] += 1
        #print(f'NAME: {names[idx]} | USED: {val}')
        new_name = f'temp_{PREFIX}_{names[idx]} {val}{ext.lower()}'
        os.rename(PATH + file, PATH + new_name)

elif MODE == 5:
    files = sort_by_x_date()
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        new_name = f'temp_{CUSTOM_NAME} {idx+1}{ext.lower()}'
        os.rename(PATH + file, PATH + new_name)

elif MODE == 6:
    files = sort_by_x_date()
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        new_name = f'temp_{PREFIX}_{CUSTOM_NAME} {idx+1}{ext.lower()}'
        os.rename(PATH + file, PATH + new_name)

trim_temp()
