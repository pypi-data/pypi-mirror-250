#cython: language_level=3

from obitools3.uri.decode import open_uri
from obitools3.apps.config import logger
from obitools3.dms import DMS
from obitools3.apps.optiongroups import addMinimalInputOption
from obitools3.dms.view.view cimport View
from obitools3.utils cimport tostr
import os
import shutil
 
__title__="Delete a view"


def addOptions(parser):    
    addMinimalInputOption(parser)

def run(config):

    DMS.obi_atexit()
    
    logger("info", "obi rm")

    # Open the input
    input = open_uri(config['obi']['inputURI'])
    if input is None:
        raise Exception("Could not read input")
    
    # Check that it's a view
    if isinstance(input[1], View) :
        view = input[1]
    else: 
        raise NotImplementedError()
    
    dms = input[0]
    
    # Get the path to the view file to remove
    path = dms.full_path  # dms path
    view_path=path+b"/VIEWS/"
    view_path+=view.name
    view_path+=b".obiview"
    
    to_remove = {}
    # For each column:
    for col_alias in view.keys():
        col = view[col_alias]
        col_name = col.original_name
        col_version = col.version
        col_type = col.data_type
        col_ref = (col_name, col_version)
        # build file name and AVL file names
        col_file_name = f"{tostr(path)}/{tostr(col.original_name)}.obicol/{tostr(col.original_name)}@{col.version}.odc"
        if col_type in [b'OBI_CHAR', b'OBI_QUAL', b'OBI_STR', b'OBI_SEQ']:
            avl_file_name = f"{tostr(path)}/OBIBLOB_INDEXERS/{tostr(col.original_name)}_{col.version}_indexer"
        else:
            avl_file_name = None
        to_remove[col_ref] = [col_file_name, avl_file_name]
    
    # For each view:
    do_not_remove = []
    for vn in dms:
        v = dms[vn]
        # ignore the one being deleted
        if v.name != view.name:
            # check that none of the column is referenced, if referenced, remove from list to remove
            cols = [(v[c].original_name, v[c].version) for c in v.keys()]
            for col_ref in to_remove:
                if col_ref in cols:
                    do_not_remove.append(col_ref)
    
    for nr in do_not_remove:
        to_remove.pop(nr)
    
    # Close the view and the DMS
    view.close()
    input[0].close(force=True)
    
    #print(to_remove)
    
    # rm AFTER view and DMS close
    os.remove(view_path)
    for col in to_remove:
        os.remove(to_remove[col][0])
        if to_remove[col][1] is not None:
            shutil.rmtree(to_remove[col][1])
        
        
