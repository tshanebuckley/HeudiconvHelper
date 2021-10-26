'''
This script to contain functions for ordering items by series_id
by splitting the serieres_id in into the series_description and 
series_number, then feeding these through a generator.

This information is pulled from and extrapolated from the
'seqinfo' that is normally looped over in a heudiconv config
file.

These are general utils. For more robust functions, look to
heud_helper/funcs.py

NOTE: must import these functions from within the infodict function
definition.

e.g. import heud_helper as heuh
heuh.get_series_ids()
'''

# import dependencies
import pathlib
import json
import os

# simply gets the list of all series_ids
def get_series_ids(seqinfo):
    '''
    Iterates through the seqinfo getting the ids 
    and returns the list of them.
    '''
    # initialize a list
    series_ids = list()
    # iterate through the seqinfo
    for idx, s in enumerate(seqinfo):
        # append the id
        series_ids.append(s.series_id)
    # return the list of series_ids
    return series_ids

# splits the id and desc and returns a dict
def split_id_and_desc(series_id):
    '''
    Base function to separate the combined dicom data
    that is concatenated to create the series_id variable.
    '''
    # initialize a dictionary
    series_dict = dict()
    # get the series number
    series_dict['num'] = series_id.split('-',1)[0]
    # get the description
    series_dict['desc'] = series_id.split('-',1)[-1]
    # return the dict
    return series_dict

# gets all of the unique series descriptions and their number of occurances
def extract_desc_info(seqinfo):
    '''
    Creates a dictionary of the unique series descriptions.
    Key(desc,protocol_name):Value(tuple of series_ids in order).
    '''
    # initialize a dictionary
    desc2count = dict()
    # loop over the items in seqinfo
    for idx, s in enumerate(seqinfo):
        # get the description of the item at this iteration
        curr_desc = split_id_and_desc(s.series_id)['desc']
        # get the current key, a tuple of the series_description and protocol_name
        curr_key = (curr_desc, s.series_description)
        # if the item does not already exist
        if curr_key not in desc2count.keys():
            # initialize it into the dict with the count being at 1
            desc2count[curr_key] = [s.series_id]
        # otherwise, the item already exists in the dict
        else:
            # increment the count for this item
            desc2count[curr_key].append(s.series_id)
    # for each item in the dictionary
    for key in desc2count.keys():
        # order the tuple and convert it to a tuple
        desc2count[key] = order_ids_by_num(desc2count[key])
    # return the dict
    return desc2count

# orders the found items of a common series description
def order_ids_by_num(series_id_list):
    '''
    Creates a dictionary from a tuple of the series description and
    protocol name to a tuple of the series ids ordered from first to
    last sequentially by scan acquisition. 
    '''
    # initialize a list
    num_list = list()
    # for each id in the list
    for id in series_id_list:
        # get the number as an int and append it to the list
        num_list.append(int(split_id_and_desc(id)['num']))
    # order the list and convert back to strings
    num_list.sort()
    num_list = [str(x) for x in num_list]
    # convert the list to a tuple
    num_tuple = tuple(num_list)
    # return the tuple
    return num_tuple

# generator that yields the next format_key assignment
def get_format_key(desc2count, key):
    '''
    Creates a generator for the given key, where the key is
    the series descrition, the then the protocol name.
    It is assumed that the of the corresponding value is 
    already ordered.
    '''
    # get the list of sorted integers as strings as a list
    sorted_series_nums = list(desc2count[key])
    # return None if the generator has run its course
    #return None
    # for each series number in the dictionary
    for num in sorted_series_nums:
        # yield the next series_id
        yield num + '-' + key[0]

# method to load the json sidecar
def load_json(heuristic, verify=True):
    '''
    Uses the a json sidecar to facilitate feeding extra information
    into the environment at run time for heudiconv.
    The json sidecar must exist next to your heuristic file.
    NOTE: this file will not be recorded under .heudiconv in
    the output directory.
    NOTE: could also be useful for saving heudiconv runtime args
    for reproducibility.
    Input must be the value of __file__ called within the heuristic file
    '''
    # get the path of the json sidecar
    json_path = pathlib.Path(heuristic).resolve().with_suffix('.json')
    # load the json file into a directory
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    # return the dict
    return json_data

# object that inherits from pydantic to verify some top-level elements exist
# NOTE: new validators may be made once data start to have nested elements
class Helper(pydantic.Base):
    '''
    Pydantic validator on the json sidecar. The purpose of this object it to
    validate data of the json sidecar along with providing required inputs that
    could be used with the Heudiconv cli or for these helper functions.
    '''
    dicom_dir: str
    out_dir: str
    dicom_path: str
