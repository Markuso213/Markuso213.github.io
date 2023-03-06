import os
import platform
import re
from datetime import date
from itertools import cycle
from importlib import reload

import utility.misc
reload(utility.misc)

replaceaao = utility.misc.replaceaao
fix_youtube_url = utility.misc.fix_youtube_url
extractNum = utility.misc.extractNum

today = date.today()
print("Today is:  {} \n".format(today))

# ╒══════════════════════════════════════════════════════════════════════════╕
# │ Cycle arrays. Used e.g for alternating black/white song/spex background. │
# └──────────────────────────────────────────────────────────────────────────┘
bigSpexButtonIDs = cycle(["two","one"])
songCycle = cycle(["two","one"])

# ╒═══════════════════════════════════════════════════════════════════════════╕
# │ Automatically find the curret work directory. All files must be relative. │
# └───────────────────────────────────────────────────────────────────────────┘
wk_dir = os.path.dirname(os.path.realpath(__file__))+'/'


# ╒════════════════════════════════════╕
# │ Starting to define functions here. │
# └────────────────────────────────────┘
def getSpexSets(spex):
    '''
    ╔───────────────────────────────────────────────────────────────╗
    │ Creates the string (VT98, VT02...) for each folder in a spex. │
    ╚───────────────────────────────────────────────────────────────╝
    '''

    sortedYear = os.listdir(os.path.join(wk_dir, "sparmen", spex))
    sortedYear.sort(key=extractNum)

    string_part_sets  = "("

    # ╒══════════════════════════════════════════════════════════════╕
    # │ Ugliest but most important. Turns 2002 to 02 and 1998 to 98. │
    # └──────────────────────────────────────────────────────────────┘
    for year in sortedYear:
        temp = year.split("_")
        string_part_sets +=temp[1] + temp[0][2:]+", "

    string_part_sets = string_part_sets[:-2]
    string_part_sets += ")"

    # ╒══════════════════════════════════════════════════════════════════════════╕
    # │ RexEx to transform naming convention in 'sparmen/spex' to shorter format │
    # └──────────────────────────────────────────────────────────────────────────┘
    string_part_sets = re.sub(r"Kivik", "S", string_part_sets)
    string_part_sets = re.sub(r"Karnevalen", "K", string_part_sets)

    # ╒════════════════════════════════════════════╕
    # │ Final touches to make spexTITLE look nice. │
    # └────────────────────────────────────────────┘
    title = re.sub(r"[_]", ". ", spex) + " " + string_part_sets

    return title

def createDivForMain():
    '''
    ╔─────────────────────────────────────────────────────────╗
    │ Div*Main wraps almost everything apart from the header. │
    ╚─────────────────────────────────────────────────────────╝
    '''
    
    # ╒════════════════════════════════════════════════════════════════════╕
    # │ Sorts all spex in 'sparmen' based on numbering via func-extractNum │
    # └────────────────────────────────────────────────────────────────────┘
    sortedSpex = os.listdir(os.path.join(wk_dir, "sparmen"))
    sortedSpex.sort(key=extractNum)

    stringDivMain = ""

    for spex in sortedSpex:
        # ╒═══════════════════════════════════════════════════════════════════╕
        # │ Cyclically add Spex*Button [Title] for expanding Spex*Div [Songs] │
        # └───────────────────────────────────────────────────────────────────┘
        stringDivMain += createBigSpexButton(spex)
        stringDivMain += createDivForSpex(spex)

    # ╒═════════════════════════════════════════╕
    # │ Return Div*Main, the outermost wrapper. │
    # └─────────────────────────────────────────┘
    return createDivMain(stringDivMain)

def createBigSpexButton(spex):
    '''
    ╔────────────────────────────────────────────────────────────╗
    │ Button with [SpexTitle] - used to expand/collapse Div*Spex │
    ╚────────────────────────────────────────────────────────────╝
    '''
    
    spexTITLE = getSpexSets(spex) # E.g., "1. En Karnevalssaga (VT98, VT02..)"

    # ╒═══════════════════════════════════════════════════════════════════════╕
    # │ ButtonString. Cycles to the next button style (one/two - black/white) │
    # └───────────────────────────────────────────────────────────────────────┘
    spexString = '''
    <button class="sp" id="{}">{}</button>
    '''.format(next(bigSpexButtonIDs), spexTITLE)

    return spexString

def createDivForSpex(spex):
    '''
    ╔───────────────────────────────────────────────────────────────────────────╗
    │ Div*Spex contains all Year*Buttons, Song*Buttons and expandable Div*Songs │
    ╚───────────────────────────────────────────────────────────────────────────╝
    '''

    # ╒═══════════════════════════════════════════════════════╕
    # │ Sorts songs according to numbering in 'sparmen/spex/' │
    # └───────────────────────────────────────────────────────┘
    sortedYears = os.listdir(os.path.join(wk_dir, "sparmen", spex)) 
    sortedYears.sort(key=extractNum)

    spexDIV = ""

    for year in sortedYears:
        # ╒═══════════════════════════════════════════════════════════════╕
        # │ Cyclically adds Year+Song*Buttons which expands each Song*Div │
        # └───────────────────────────────────────────────────────────────┘
        
        yearString =  createYearButton(spex, year)
        yearString += createDivForSongs(spex, year)

        spexDIV += yearString

    spexDIV += createBlocker() # Marks end of spex

    spexDIV = '''
        <div class="content">
        {}
        </div>
        '''.format(spexDIV)

    return spexDIV

def createBlocker():
    '''
    ╔────────────────────────────────────────────────────────────────────────╗
    │ createBlockers only function is to add a colored line at "End of Spex" │
    ╚────────────────────────────────────────────────────────────────────────╝
    '''
    
    blockerSTRING = '''<button class="sb"
    style="background-color:orange;color:white;text-align:left;font-weight:bold;font-size:2;"></button>
    '''
    return blockerSTRING


def createYearButton(spex, year):
    '''
    ╔───────────────────────────────────────────────────────────────────────╗
    │ function which creates a given Year*Button (it has zero functionality │
    ╚───────────────────────────────────────────────────────────────────────╝
    '''
    
    # ╒════════════════════════════════════════════════════════════════════╕
    # │ RegEx to extract yearTITLE (e.g 2002) from 'sparmen/spex/year_sem' │
    # └────────────────────────────────────────────────────────────────────┘
    yearTITLE = re.sub(r"_.+", " ", year)
    yearTITLE = re.sub(r"[-]*.txt", "", yearTITLE)

    titleBox = '''<button class="sb"
    style="background-color:#1a1a1a;color:white;text-align:left;font-weight:bold;font-size:20;border-left:2px-solid-red;">{}</button>
    <div class="empty" id="three"></div>'''.format(yearTITLE)

    return titleBox

def createSongButton(title):
    oneSong = '''
      <button class="sb" id="{}">{}</button>
    '''.format(next(songCycle), title)
    return oneSong

def createDivForSong(text):
    '''
    ╔────────────────────────────────────────────────────────────────────╗
    │ Song*Div which contains lyrics, melody etc. The innermost wrapper. │
    ╚────────────────────────────────────────────────────────────────────╝
    '''
    
    # ╒══════════════════════════════════════════════════════════╕
    # │ class="song" is used for styling purposes with CSS later │
    # └──────────────────────────────────────────────────────────┘
    div =  '''
          <div class="song">
            {}
          </div> 
          '''
    try:
        div = div.format(text)
    except:
        print("createDivForSong failed for:\n {}   {}   {}".format(spex, year, song))

    return div

def createDivForSongs(spex, year):
    sortedSongs = os.listdir(os.path.join(wk_dir, "sparmen", spex, year)) 
    sortedSongs.sort(key=extractNum)

    yearDIV = ""

    for song in sortedSongs:
        songURL = os.path.join(wk_dir, "sparmen", spex, year, song)
       

        # ╒══════════════════════════════════════════════╕
        # │ Reads the songTXT from the local harddrive   │
        # └──────────────────────────────────────────────┘
        f = open(songURL, "r+", encoding="utf8")
        print(songURL)
        songTXT = f.read()
        f.close()

        # ╒═════════════════════════════════════════════════════════╕
        # │ RegEx which extracts songTITLE from 'sparmen/spex/year' │
        # └─────────────────────────────────────────────────────────┘

        firstLine = songTXT.split("\n")
        firstLine = firstLine[0]
        songTITLE = re.sub(r".txt", ". " + firstLine, song)
        # songTITLE = firstLine

        # ╒══════════════════════════════════════════════════════════╕
        # │ Replace \n with HTML-compatible <br> throughout the song │
        # └──────────────────────────────────────────────────────────┘
        songTXT = re.sub(r'\n', '<br>', songTXT)
        
        # ╒════════════════════════════════════════════╕
        # │ Cyclically create Song*Button and Song*Div │
        # └────────────────────────────────────────────┘
        yearDIV += createSongButton(songTITLE)
        yearDIV += createDivForSong(songTXT)

    # ╒════════════════════════════════════════════════════════════════════╕
    # │ spexstring should contain all years - which in turn are in yearDIV │
    # └────────────────────────────────────────────────────────────────────┘
    spexString = '''
        {}
        '''

    return spexString.format(yearDIV)

def createDivMain(content):
    '''
    ╔─────────────────────────────────────────────────────────╗
    │ Div*Main wraps almost everything apart from the header. │
    ╚─────────────────────────────────────────────────────────╝
    '''

    divString = '''
        <div class="main">
        {}
        </div>
    '''.format(content)

    return divString


def createFullWebPage(wk_dir = wk_dir, targetFile = "index.html"):
    f = open(wk_dir + 'pageTemplate.html', 'r')
    webPageTemplate = f.read()
    f.close()

    webPageString = re.sub(r'MONSTERSTRINGHERE', createDivForMain() , webPageTemplate)
    webPageString = replaceaao(webPageString)
    webPageString = re.sub(r'DATUM', 'Uppdaterad: {}'.format(today),webPageString)

    targetURL = os.path.join(wk_dir, "index.html")

    print('Attempting to write {}. \n\t Full path: {}'.format("index.html",
        targetURL))

    w = open(targetURL, 'w', encoding="utf8")
    w.write(webPageString)
    w.close()

if __name__ == "__main__":
    createFullWebPage()

