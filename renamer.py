import os

"""
mode
1 - add prefix, add index
2 - add prefix, keep original name
3 - add custom name, add index
4 - add prefix, add custom name, add index
5 - trim first found prefix
"""

mode = 4
prefix = 'f'
custom_name = 'art'
sort_by_created_date = False
sort_by_modified_date = True
allowed_formats = [ '.mp4', '.mov', '.avi', '.png', '.jpg' ]

if (
    type(mode) is not int
    or
    type(prefix) is not str
    or
    type(custom_name) is not str
    or
    type(sort_by_created_date) is not bool
    or
    type(sort_by_modified_date) is not bool
    or
    (
        sort_by_created_date == True
        and 
        sort_by_modified_date == True
    )
    or
    prefix == ''
    or
    custom_name == ''
):
    exit()
else:
    if sort_by_created_date == True:
        sort_mode = 1
    elif sort_by_modified_date == True:
        sort_mode = 2
    else:
        sort_mode = 0

def sort_by_x_date(enabled:'int'=0) -> 'list':
    if enabled > 0:
        this_path = os.getcwd()
        files = []
        for file in os.listdir():
            files.append(this_path + '\\' + file)
        
        if enabled == 1:
            files.sort(key=os.path.getctime)
        elif enabled == 2:
            files.sort(key=os.path.getmtime)
            
        return files
    elif enabled == 0:
        return os.listdir()

def trim_prefix():
    success, total = 0, len(os.listdir()) - 1
    skipped = []
    for file in os.listdir():
        name, ext = os.path.splitext(file)
        pos = name.find('_')
        if pos == -1 or ext.lower() not in allowed_formats:
            skipped.append(''.join(name + ext))
            continue
        success+=1
        name = name[pos+1:]
        new_name = f'{name}{ext.lower()}'
        os.rename(file, new_name)
        
    print(f'[{success}/{total}] trimmed\nSkipped: {skipped}')
        
if mode == 1:
    trim_prefix()
    files = sort_by_x_date(sort_mode)
    for idx, file in enumerate(files):
        name, ext = os.path.splitext(file)
        if ext.lower() not in allowed_formats:
            continue
        new_name = f'{prefix}_{idx+1}{ext.lower()}'
        os.rename(file, new_name)

elif mode == 2:
    trim_prefix()
    files = sort_by_x_date(sort_mode)
    for file in files:
        name, ext = os.path.splitext(file)
        if ext.lower() not in allowed_formats:
            continue
        new_name = f'{prefix}_{name}{ext.lower()}'
        os.rename(file, new_name)

elif mode == 3:
    trim_prefix()
    files = sort_by_x_date(sort_mode)
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        if ext.lower() not in allowed_formats:
            continue
        new_name = f'{custom_name}_{idx+1}{ext.lower()}'
        os.rename(file, new_name)

elif mode == 4:
    trim_prefix()
    files = sort_by_x_date(sort_mode)
    for idx, file in enumerate(files):
        _, ext = os.path.splitext(file)
        if ext.lower() not in allowed_formats:
            continue
        new_name = f'{prefix}_{custom_name}_{idx+1}{ext.lower()}'
        os.rename(file, new_name)

elif mode == 5:
    trim_prefix()