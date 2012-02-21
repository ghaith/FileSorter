'''
Created on Feb 20, 2012

@author: ghaith
'''

import Sorter


if __name__ == '__main__':
    sorter = Sorter.Sorter('/media/Expansion Drive/B','/media/Expansion Drive/Sorted Backup')
    sorter.parseFiles()
    print "Finished Execution"
    