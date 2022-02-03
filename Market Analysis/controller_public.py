# ========================================================================
# Controller Module - Market Analysis
#     Written by Patrick Keener
#
# The purpose of this module is to control execution of each step in the 
# trading management system.
#
# This program has the following dependencies:
# Pandas, Numpy, SKLearn, SKTime, Quandl
#  Generate requirements via pipreqs file
# ========================================================================
import sys

# ========================== Define Settings Class =======================

class programSettings():
    ''' Contains settings used throughout the program'''
    def __init__(self):
        
        # Define location of other scripts used in this module
        self.scriptPath = r'C:\Users\smpat\OneDrive\Trading'
        
        # Define CUSTOM modules (imported for settings.scriptpath)
        self.modListCust = ['dataManagement']

        # Define STANDARD packages; ensures proper loading each run
        # broken out from above for easier maintenance
        self.modListStandard = ['pandas', 'numpy', 'sklearn', 'quandl', 'json'
                                ,'sys', 'time']

        self.modList = self.modListCust + self.modListStandard

        #=== Set parameters
        
        # Sharadar Params
        self.bulkDownSharadar = False #bulk download for Sharadar
        self.apiKeySharadar = ##### #sharadar access key goes here
        
        # SF1 is primary table
        self.tableListSharadar = ['SF1', 'DAILY', 'TICKERS', 'INDICATORS'
                                 ,'ACTIONS', 'SP500', 'EVENTS'] 
        
        self.dataLocSharadar = r'"C:\tradingData\Sharadar\SHARADAR_'








# =======================================================================
# =======================================================================

# Add folder path to list for imports
def environPrep(settings):
    # Prepares environment to accept new modules
    ''' Preliminary methods for modules '''

    print("Prepping environment:\n")
    
    # Add filepath where scripts can be found
    if settings.scriptPath not in sys.path:
        sys.path.append(settings.scriptPath)
        print("Subscript path added to system path")
    else: print("Subscript path found\n")

    # Ensure all modules are unloaded
    unloadCount = 0
    for mod in settings.modList:
        if mod in sys.modules:
            unloadCount += 1
            del sys.modules[mod]
            print(str("{} module unloaded").format(mod))
    if unloadCount == 0:
        print("No modules unloaded\n")
    else:
        print("Unloading complete\n\n")
    
    return None




def executeDataStep(settings):
    ''' Executes the data step '''
    import dataManagement 
    dataManagement.main(settings)

    return None


def main():
    # Controller Module
    ''' Coordinates & controls program execution '''

    settings = programSettings() # Initialize settings object
    environPrep(settings) # Prepare environment for code execution

    # Execute the data step
    #executeDataStep(settings)


    return None



main()




