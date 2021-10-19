from utils import *

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
