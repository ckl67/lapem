# ######################################################
# Christian Klugesherz
# March 2020
# ######################################################
from os import listdir,rename,getcwd
from os.path import isfile, isdir, join, splitext, exists
import sys

# ######################################################
# Global Vars
# ######################################################

APPLICATION_DEBUG_LEVEL = 0

# ######################################################
# Functions Prototype
# ######################################################
# def setApplicationDebugLevel(val):
# def getApplicationDebugLevel():
# def pError(text):
# def pDbg(text,functDlv=0,appDLv=0):
# def pDbg0(text):
# def pDbg1(text):
# def pDbg2(text):
# def pDbg3(text):
# def pDbg4(text):
# def pDbg5(text):
# def pFlaskAppConf(my_dict, printAll=False):
   
# ######################################################
# Functions
# ######################################################

# -----------------------------------------------------
# Set and Get application Debug Level
# -----------------------------------------------------

def setApplicationDebugLevel(val):
    ''' 
    set Global variable: APPLICATION_DEBUG_LEVEL
    '''
    global APPLICATION_DEBUG_LEVEL
    APPLICATION_DEBUG_LEVEL = val
    pDbg1("(setApplicationDebugLevel) Set Application Debug Level: {0}".format(APPLICATION_DEBUG_LEVEL))

def getApplicationDebugLevel():
    ''' 
    get Global variable: APPLICATION_DEBUG_LEVEL
    '''
    pDbg1("(getApplicationDebugLevel) Debug Level: {0}".format(APPLICATION_DEBUG_LEVEL))
    return (APPLICATION_DEBUG_LEVEL)

# -----------------------------------------------------
# Print Error 
# -----------------------------------------------------
def pError(text):
    '''
    Print Error
    '''
    out = "!! ERROR: "+ text + " !!"
    for x in range(len(out)):
        print('-', end='')
    print()
    print(out)
    for x in range(len(out)):
        print('-', end='')
    print()
    
# -----------------------------------------------------
# Display the 'text' in the consol for debugging usage.
# text will be displayed as soon
# application debug level is >= than the level in the function
# -----------------------------------------------------
def pDbg(text,functDlv=0,appDLv=0):
    '''
    Display the 'text' in the consol for debugging usage.
    We have to consider 2 parameters :
      * appDLv 
            The Overall debug level needed by the application
            For exemple : app.config["WEBAPP_DEBUG_LEVEL"] = 3
      * functDlv
            The Debug level for information to display in the function 
       --> text will be displayed as soon application debug level is >= than the level in the function
    Exemple
       def test()
            ....    
            pDebg("Value of i="+i,3,appDLv)
            ....
       --> means if appDLv>=3, then the information will be dispayed, otherwise not
    '''
    if appDLv >= functDlv :
        print(text)
        
# -----------------------------------------------------
# Print debug level 0 == like print()
# BUT THIS FUNCTION CAN BE EMPTY ONCE THE CODE IS PERFECT
# IT IS A TRICK TO DISPLAY THE INFORMATION ONCE APPLICATION_DEBUG_LEVEL IS NOT KNOWN
# -----------------------------------------------------
def pDbg0(text):
    '''
    idem as pDbg(text,0,APPLICATION_DEBUG_LEVEL) 
    '''
    pDbg(text,0,APPLICATION_DEBUG_LEVEL)

        
# -----------------------------------------------------
# Print debug level 1
# -----------------------------------------------------
def pDbg1(text):
    '''
    idem as pDbg(text,1,APPLICATION_DEBUG_LEVEL)
    '''
    pDbg("  "+text,1,APPLICATION_DEBUG_LEVEL)
    
# -----------------------------------------------------
# Print debug level 2
# -----------------------------------------------------
def pDbg2(text):
    '''
    idem as pDbg(text,2,APPLICATION_DEBUG_LEVEL)
    '''
    pDbg("    "+text,2,APPLICATION_DEBUG_LEVEL)
    
# -----------------------------------------------------
# Print debug level 3
# -----------------------------------------------------
def pDbg3(text):
    '''
    idem as pDbg(text,3,APPLICATION_DEBUG_LEVEL)
    '''
    pDbg("      "+text,3,APPLICATION_DEBUG_LEVEL)

# -----------------------------------------------------
# Print debug level 4
# -----------------------------------------------------
def pDbg4(text):
    '''
    idem as pDbg(text,4,APPLICATION_DEBUG_LEVEL)
    '''
    pDbg("        "+text,4,APPLICATION_DEBUG_LEVEL)

# -----------------------------------------------------
# Print debug level 5
# -----------------------------------------------------
def pDbg5(text):
    '''
    idem as pDbg(text,5,APPLICATION_DEBUG_LEVEL)
    '''
    pDbg("          "+text,5,APPLICATION_DEBUG_LEVEL)

# -----------------------------------------------------
# function which rename all files in a directory by replacing : charin by charout
# -----------------------------------------------------
def renFileDir(dirin,charin,charout):
    """
    function which rename all files in a directory by replacing : charin by charout
    parameters
    * dirin : absolute or relative directory path
    * charin : characters to replace
    * charout : character to replace
    Return the number of files which have been converted, or -1 if issue
    """

    retval = 0
    pDbg4("(renFileDir): Rename all files containing '{0}' by '{1}' in directory {2}".format(charin,charout,dirin) )

    # test if Directory exists
    if not exists(dirin):
        pError("(renFileDir): chek if : " + dirin +" exists")
        retval = -1
        return retval
       
    for f in listdir(dirin): # lis all of item in a directory
        if isfile(join(dirin, f)): # Check if 'f' it is file
            pDbg5("(renFileDir): Checking file: "+ f)
            if f.find(charin) > 0:   # Check if in the file there is charin ?
                fout = f.replace(charin,charout)
                retval = retval+1
                pDbg5("(renFileDir): --> new file="+ fout)
                rename(join(dirin, f),join(dirin, fout))
    return retval

# -----------------------------------------------------
# function which rename all files in all Sub directory by replacing : charin by charout
# -----------------------------------------------------
def renFileSubdir(dirin,charin,charout):
    """
    function which will rename all files in all Sub directories of a Directory by replacing : charin by charout
    Parameters
    * dirin : absolute or relative directory path
    * charin : characters to replace
    * charout : character to replace
    Return the number of files which have been converted, or -1 if issue
    """

    retval = 0
    pDbg3("(renFileSubdir): Rename all files containing '{0}' by '{1}' in directory {2}".format(charin,charout,dirin) )

    if not exists(dirin):
        pError("(renFileSubdir): chek if : " + dirin +" exists")
        retval = -1
        return retval
    
    for d in listdir(dirin): # lis all of item in a directory
        pDbg4("(renFileSubdir): Checking dir :" + d)
        if isdir(join(dirin, d)): # Check if it is directory
            retval = retval + renFileDir(join(dirin, d),charin,charout)
    return retval


# -----------------------------------------------------
# function which retrurn the number of file type in a directory
# -----------------------------------------------------
def cntExtFileDir(dirin,fext):
    """
    function which return the number of file type in a directory 
    parameters
    * dirin : absolute or relative directory path
    * fext  : file extension
    Return the number of files which have been converted, or -1 if issue
    """

    retval = 0
    pDbg4("(cntExtFileDir): Count all files with extension '{0}' in directory {1}".format(fext,dirin) )

    # test if Directory exists
    if not exists(dirin):
        pError("(cntExtFileDir): chek if : " + dirin +" exists")
        retval = -1
        return retval
       
    for f in listdir(dirin): # lis all of item in a directory
        if isfile(join(dirin, f)): # Check if 'f' it is file
            pDbg5("(cntExtFileDir): Checking file: "+ f)
            filename, file_extension = splitext(f)
            if file_extension == fext :  
                retval = retval+1
    return retval


# -----------------------------------------------------
# function which rename all Directories in a directory by replacing : charin by charout
# -----------------------------------------------------
def renSubDir(dirin,charin,charout):
    """
    function which rename all Directories in a directory by replacing : charin by charout
    Parameters
    * dirin : absolute or relative directory path
    * charin : characters to replace
    * charout : character to replace
    Return the number of files which have been converted, or -1 if issue
    """

    retval = 0
    pDbg3("(renSubDir): Rename all directories containing '{0}' by '{1}' in directory {2}".format(charin,charout,dirin) )

    if not exists(dirin):
        pError("(renSubDir): chek if : " + dirin +" exists")
        retval = -1
        return retval
  
    for f in listdir(dirin): # lis all of item in a directory
        if isdir(join(dirin, f)): # Check if it is directory
            pDbg4("(renSubDir): Checking dir :" + f)
            if f.find(charin) > 0:   # Check if in the file there is charin ?
                fout = f.replace(charin,charout)
                rename(join(dirin, f),join(dirin, fout))
                pDbg4("(renSubDir): --> new directory ="+ fout)
                retval = retval+1
    return retval

# -----------------------------------------------------
#    Format the command to send to os.system
# -----------------------------------------------------
def formatCmd2os(cmd):
    '''
    Format the command to send to os.system
    Example: 
        Aigle_D'Or,_Le_(1983) is a correct name for a Directory, or file: This data is saved in oricdic
    However, for a Linux command the chars: "'", or "(", or ")" are not allowed alone, so we must add prefix "\"
    Auto-completion in Linux will give
        >>:~/Work/Orpic/src/webapp/static/Tapes$ ls Aigle_D\'Or,_Le_\(1984\)/
    For example we will replace an (apostrophe) ' by \' in order to make a "cd"
    '''
    pDbg3("(formatCmd2os): in="+ cmd)

    out = cmd
    out = out.replace("'","\\'")
    out = out.replace("(","\(")
    out = out.replace(")","\)")

    pDbg3("(formatCmd2os): out="+ out)
    return(out)


def pFlaskAppConf(my_dict, printAll=False):
    '''
    Print the configuration information for Flask app.Config instance !
    We will check the Debug Level to display the information
        "WEBAPP_DEBUG_LEVEL" > 1 then the information is displayed
    '''

    DList = [
        "WEBAPP_DEBUG_LEVEL",
        "WEBAPP_VERSION",
        "DEBUG",
        "TAP2WAV_FORM_BAUD_ID",
        "TAP2WAV_FORM_FREQUENCE_ID",
        "TAP2WAV_FORM_SPLIT_ID",
        "TAP2WAV_VERSION"
    ]

    if my_dict["WEBAPP_DEBUG_LEVEL"] > 1:
    
        if printAll == True:
            for item in my_dict:
                print("{0} = {1}".format(item,my_dict[item]))
        else:
            for item in my_dict:
                for vl in DList:
                    if vl == item:
                        print("{0} = {1}".format(item,my_dict[item]))
    
                    
# ######################################################
# TESTS
# ######################################################
           
if __name__ =='__main__':
    # Test print debug level functions
    setApplicationDebugLevel(3)
    print("\nWill test print debug level functions (pDbg) with overall Applicationn Debug Level={0}".format(getApplicationDebugLevel()))
    pError("Something is going wrong here")
    pDbg0("Debug level 0")
    pDbg1("Debug level 1")
    pDbg2("Debug level 2")
    pDbg3("Debug level 3")
    pDbg4("Debug level 4")
    pDbg5("Debug level 5")

