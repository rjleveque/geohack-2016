
"""
Set top_dir to the absolute path to the top level of this git repository.
Adjust if necessary below...
"""

import os,sys

#---------------------------------------------------------------------
# Adjust this line if needed to set path properly:
top_dir = os.path.abspath('..')
# Should be right when this module is imported from Notebooks subdirectory.
#---------------------------------------------------------------------

print "Assuming that top level of this repository is at: %s" % top_dir

codes_dir = os.path.join(top_dir, 'PythonCode')
print "    Python codes can be found in codes_dir = %s"  % codes_dir
sys.path.append(top_dir)   # make python modules available

data_dir = os.path.join(top_dir, 'DataFiles')
print "    Data files can be found in data_dir = %s"  % data_dir

