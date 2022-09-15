import json
from dsutils.de.filesystem import *
from dsutils.de.utils import *
import fnmatch
import functools
import os
import shutil
from tqdm import tqdm


def get_dir_and_doc_paths(path):
    if os.path.isfile(path):
        dir_path = get_parent_dir(path)
        filepath = path
    elif os.path.isdir(path):
        dir_path = path
        filepath = get_child_ext_path(dir_path=dir_path, ext='pdf')
    else:
        print('enter an existing path')
    return dir_path, filepath

def join_parentpath_childnames(parentpath,childnames):
    fullpaths = map(functools.partial(os.path.join,
                        parentpath),
        childnames)
    return list(fullpaths)


# lists paths with certain extension 
def list_ext(path,
            exts,
            invert=False): # return files WITHOUT such extensions instead
    path_list = list()
    for ext in exts:
        if type(ext) == list:
            ext = ext[0]
        for filename in os.listdir(path):
            filepath = os.path.join(path,filename)
            ends_ext = filepath.endswith(ext)
            is_file = os.path.isfile(filepath)
            has_ext = ends_ext and is_file
            if not invert:
                ret_ext = has_ext 
                if ret_ext:
                    path_list.append(filepath)
            elif is_file:
                ret_ext = not has_ext
                if ret_ext:
                    path_list.append(filepath)
    return path_list

# get one child with requested extension
def get_child_ext_path(dir_path, ext):
    child = list_ext(path=dir_path,exts=[ext])[0]
    return child

# creates a folder with the document's name and moves the document in it
def mv_to_custom_dir(doc_path):
    split_path = os.path.split(doc_path)
    ext = os.path.splitext(doc_path)[-1]
    new_dir_name = split_path[-1][:-len(ext)] # same as filename, without the extension
    filename = split_path[-1]
    input_dir_path = split_path[-2]

    new_dir_path = os.path.join(input_dir_path,new_dir_name.replace(" ", "_"))
    new_doc_path = os.path.join(new_dir_path,filename.replace(" ", "_"))

    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path)
    if not os.path.exists(new_doc_path):
        os.rename(doc_path,new_doc_path)
    else:
        print('Warning: a document named {0} already exists. Deleting the newer copy.'.format(filename))
        os.remove(doc_path)
    return
def get_parent_dir(path):
    return os.path.split(path)[-2]

def get_child_dir_paths(dir_path):
    child_names = os.listdir(dir_path)
    child_paths = [os.path.join(dir_path,child_name) for child_name in child_names]
    dir_paths = [child_path for child_path in child_paths if os.path.isdir(child_path)]
    return dir_paths

# make directory if it doesn't exist
def mkdir_no_over(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name
    
def save_file(filepath, data):
    with open(filepath, 'w+') as f:
        f.write(data)

def save_data(doc_dir,
                dir_name,
                file_name,
                content,
                ):
    dirpath = os.path.join(doc_dir,dir_name)
    mkdir_no_over(dir_name)
    filepath = os.path.join(dirpath,file_name)
    save_data(filepath, content)
    
def get_final_files(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        goodfiles = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in goodfiles)
    print('{0} FILES FOUND'.format(len(results)))
    return results

def store_final_files(final_name, data_path, target_folder):
    final_files = get_final_files(data_path, final_name)
    for t in tqdm(final_files, desc='files stored', leave=False):
        path = os.path.normpath(t)
        path_sects = path.split(os.sep)
        target_name = path_sects[-3]+'_'+final_name
        target_path = os.path.join(target_folder,target_name)
        shutil.copyfile(t, target_path)

def try_read(path, ext=None, alt=''):
    try:
        if ext is None:
            filepath = path
        else:
            filepath = get_child_ext_path(path, ext)
        with open(filepath) as f:
            content = f.read()
    except (IndexError, FileNotFoundError):
        content = alt
    return content

def store_data(storage,
                data,
                dir_path,
                name):
    storage_types = ['meta', # the metadata file
                    'dir'] # a new subdirectory where the document is stored
    if storage not in storage_types:
        raise ValueError("Invalid path_type. Expected one of: {0}".format(storage_types)) 
    
    if data:
        match storage:
            case 'meta':
                data_path = os.path.join(dir_path,name+'.json')
                with open(data_path, 'w+') as f:
                    json.dump(data, f)
            case 'dir':
                if type(data) == dict:
                    for k,v in data.items():
                        new_dir = mkdir_no_over(os.path.join(dir_path,k))
                        data_path = os.path.join(new_dir, name+'.txt')
                        with open(data_path, 'w+') as f:
                            f.write(v)  
                else:
                    new_dir = mkdir_no_over(os.path.join(dir_path,name))
                    data_path = os.path.join(new_dir, get_var_name(data)+'.txt')
                    with open(data_path, 'w+') as f:
                        f.write(data)
    else:
        data_path = ''
    return data_path
