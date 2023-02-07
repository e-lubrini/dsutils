from ast import operator
import imp
import json
from dsutils.de.utils import dbg, get_var_name
import fnmatch
import functools
import os
import shutil
from tqdm import tqdm
import pandas as pd
import sys
import subprocess

#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tabulate'])
from tabulate import tabulate

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

# find first data subdir in path
def get_data_path(wd = os.getcwd()):
    dircount = 0
    dirs = list(wd.split(os.path.normpath(os.sep)))+['data']
    for i in range(len(dirs)):
        data_dir = os.path.normpath(os.sep)+os.path.join(*list(dirs[:-i]),'data')
        if os.path.isdir(data_dir):
            return data_dir
        else:
            dircount += 1
    return None

def get_datafile_path(filename, data_path=get_data_path(), format='csv'):
    filepath = os.path.join(data_path,filename)
    if '.xls' in filename and 'csv' in format :
        filepath = xls_to_csv(filepath)
    return filepath
        
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

def xls_to_csv(xls_path, csv_path=''):
    read_file = pd.read_excel(xls_path)
    if not csv_path:
        csv_path = os.path.join(get_parent_dir(xls_path),os.path.splitext(os.path.basename(xls_path))[0]+'.csv')
    read_file.to_csv(csv_path, index = None, header=True)
    return csv_path

def get_filename(path):
    filename = os.path.basename(path)
    return filename
def get_extension(path):
    ext = os.path.splitext(path)[-1]
    return ext

def sample_csv(path, size=5, filename='', in_col_select_rows={}, operator='OR'):
    if not filename:
        filename = get_filename(path)
    sample_path = filename+'_sample'+get_extension(path)
    df = pd.read_csv(path)
    df_ = None
    if in_col_select_rows:
        if operator == 'OR':
            for c,strs in in_col_select_rows.items():
                dbg(c)
                c =0
                for s in strs:
                    c +=1
                    dbg(s)
                    if c>1:
                        quit()
                    if type(df_) == None:
                        print('NONE')
                        df_ = df[df[c].astype(str).str.contains(s, na = False)]   
                    else:
                        df_ = pd.concat([df_, df[df[c].astype(str).str.contains(s, na = False)]])
                    print(set(df_['id']))
            df = df_
        elif operator == 'AND':
            for c,strs in in_col_select_rows.items():
                for s in strs:
                    df = df[df[c].astype(str).str.contains(s, na = False)]
    df.head(size).to_csv(sample_path, index = None, header=True)
    return sample_path

def get_csv_head(path, size=5, nrows=100):
    with open(path) as f:
        df = pd.read_csv(f, on_bad_lines='skip', nrows=nrows)
    if isinstance(size, str):
        return df
    return df.head(size)


def describe_csv(path):
    df = pd.read_csv(path, on_bad_lines='skip')
    return df.describe(include="all") #pd.DataFrame(df, c = df.shape),
