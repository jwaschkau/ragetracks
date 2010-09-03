# _*_ coding: UTF-8 _*_
###########################################################
## this module loads a language file
###########################################################

import os, os.path
from configobj import ConfigObj

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

def getAvailableLanguages():
    '''
    @return: returns a list with all available language names
    '''
    files = os.listdir("data/language")
    names = []
    for f in files:
        if f[-5:] == ".lang":
            names.append(f[:-5])

    return names


# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

class Language(object):
    '''
    this class opens a language file
    '''
    def __init__(self, language):
        '''
        @param language: (str) name of the language file (without extension)
        '''
        # check if the language is a string
        if type(language) != str:
            raise typeError("language has to be of type 'str'")

        # okay, save some details
        self.language = language
        filename = "data/language/"+language+".lang"

        # check if the file is available
        if not os.path.isfile(filename):
            raise ioError("language file could not be found")

        # read the words out of the file
        self.words = ConfigObj(filename)

    # ---------------------------------------------------------

    def __getitem__(self, index):
        '''
        returns the item at the given index
        for using this class with Language["menu"]["options"]
        '''
        # if the word is in the file, return it
        if index in self.words:
            return self.words[index]

        # else return a string with three question signs
        else:
            return "???"

    # ---------------------------------------------------------

    def __str__(self):
        '''
        represents the class for printing
        '''
        return "Language("+self.language+")"

    # ---------------------------------------------------------

    def getLanguageName(self):
        '''
        @return: returns the name of the language as a tupel (file name, native name)
        '''
        return (self.language, self.words["language"])

    # ---------------------------------------------------------


# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------


# Test the module
if __name__ == "__main__":
    print "Avalilable languages:", getAvailableLanguages()

    lang = Language("german")
    print "Chosen language: ", lang.getLanguageName()
    print "\n"
    print "new_game in this language:", lang["menu"]["new_game"]
