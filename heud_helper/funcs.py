'''
The purpose of this file is to expand upon utils into functions that allow for the 
meeting certain use cases.

Some use cases these functions plan to tackle:
1. Getting the directory name of a scan, as there are some instances where this would
make using Heudiconv more user friendly.
2. Accessing dicom header metadata beyond what is included in the .tsv under the .heudiconv cache.
This would most likely be done by using pydicom.
3. Applying the IntendedFor field to the output json sidecars (may require some atexit shenanigans
as this would obviously need to run after Heudiconv is finished).
4. Would also like to allow for a general json sidecar updater as there is other metadata that may
need fed forward from dicoms or from study knowlegde that could be set in the HeudiconvHelper sidecar.
5. More robust logs. Heudiconv stores which files were selected for which scan. Would be nice
to also include a note or log of file not selected from the raw data as a check.

NOTE: will probably look to dcm2bids for inspiration on more features.
'''

from .utils import *

# method to get the actual directory name from the data in seqinfo and the path to the directory
# TODO: finish
def seqinfo_to_dirname(json_data):
    # initialize a dictionary
    series_id2dir = dict()
    # the directory the heuristic file would be the path of the metadata
    meta_path = os.path.dirname(cfg_path)
    # the subject id will be the basename of the metadata path
    subj_id = os.path.basename(meta_path)
    # path to the json file in the metadata
    json_path = meta_path + '/filegroup.json'
    # load the json file into a directory
    with open(json_path, 'r') as f:
        filegroup_dict = json.load(f)
    # print the filegroup to test for now
    print(filegroup_dict)
