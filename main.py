from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from hanzidentifier import is_traditional

# look into pickle to save data without needing to scrape every time


# Class for single characters
class Character:
    instances = []

    def __init__(self, character, MBlevel) -> None:
        self.id = len(Character.instances) + 1
        self.string = character
        self.MBlevel = MBlevel

        # 0: both, 1: simplified, 2: traditional
        # since we know is_simplified == True, we only need to check if also traditional
        self.simplifiedStatus = 0 if is_traditional(self.string) else 1
        
        Character.instances.append(self)

    @classmethod
    def printClass(cls):
        print([f'{i.string}' for i in cls.instances])




# Class for words, including single character words
class Word:
    instances = []

    def __init__(self, word, MBlevel) -> None:
        self.id = len(Word.instances) + 1
        self.string = word
        self.MBlevel = MBlevel
        self.characters = [] #TODO
        
        # 0: both, 1: simplified, 2: traditional
        self.simplifiedStatus = 0 if is_traditional(self.string) else 1

        Word.instances.append(self)


    @classmethod
    def printClass(cls):
        print([f'{i.string}' for i in cls.instances])

# create a json file that contains all words & characters up to and including a specified level for Migaku known word list
# I include characters because otherwise single characters will be marked as unknown in Migaku
def exportToMigaku(maxLevel, path=None):
    # list that gets exported
    exportList = []
    # set that keeps track of used characters to avoid duplicates between single characters and words
    usedCharacters = set()
    # loop through words until maxLevel is reached
    for wordObj in Character.instances + Word.instances:
        
        word = wordObj.string

        # there is an error on the traverse website where character 1795 is a unreadable part, so I remove it manually here
        if word == '狭':
            word = '狭'
        
        if (wordObj.MBlevel == maxLevel + 1) or (word in usedCharacters):
            continue
        
        # format required by Migaku. Number after ◴ indicates if character is both, simplified, traditional
        # including this is required for Migaku to work properly. The number at the end means the word is already learnt
        exportList.append([f"{word}◴{wordObj.simplifiedStatus}", 2])
        usedCharacters.add(word)
    
    # default path
    if path == None:
        path = f'./migaku_known_words/MB_knownWords_level_{maxLevel:02d}.json'

    # write to file
    with open(path, 'w') as file:
        # must replace all ' with " for Migaku to parse
        file.write(str(exportList).replace("'", "\""))

try:
    # Set up Firefox options for headless browsing
    firefox_options = Options()
    firefox_options.headless = True  # Run Firefox in headless mode (no GUI)

    # Initialize the Firefox driver with the specified options
    # Using firefox instead of chrome because simpler with WSL (no separate binaries needed)
    driver = webdriver.Firefox(options=firefox_options)

    # loop over every MB level 1 -> 88
    for level in range(1, 89):
        # URL of the website
        url = 'https://traverse.link/Mandarin_Blueprint/word-progress/?level=' + str(level)

        # Open the website in the headless Firefox browser
        driver.get(url)

        # Wait for a specific element to be present (in this some new characters under the all characters header)
        wait = WebDriverWait(driver, 20)  # Wait for up to 10 seconds
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'h3[id="All Characters"] + .MuiGrid-container > .MuiGrid-item .text-red-600')))
        
        # will extract the new words and characters from each of the following
        # headings (categories) for each level
        categories = {"All Characters":[], "All Words":[],"Nouns 名词":[], "Verbs 动词":[], "Adjectives 形容词":[], "Adverbs 副词":[], 
                    "Pronouns 代词":[], "Measure 量词":[], "Numbers 数词":[], "Prepositions 介词":[], 
                    "Conjunction 连词":[], "Particles 助词":[], "Mood 语气词":[]}
        
        # loop over the different categories
        for category in categories:
            
            # extract the new entries for each category
            elements = driver.find_elements(By.CSS_SELECTOR, f'h3[id="{category}"] + .MuiGrid-container > .MuiGrid-item .text-red-600')

            # Extract the text content of all elements
            categories[category] = [element.text for element in elements]


        # Convert characters and words into new Character and Word objects
        for newChar in categories['All Characters']:
            Character(newChar, level)

        for newWord in categories['All Words']:
            Word(newWord, level)

        # Create Migaku Export for current level
        print(level)
        exportToMigaku(level)


# if something goes wrong show it
except Exception as e:
    print(e)

# to make sure the browser is closed regardless of an error or not
finally:
    # Close the browser
    driver.quit()