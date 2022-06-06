from cmath import phase
from email.policy import default
import json
import numpy as np

strategy = 1 
phase = 1
epoch = 0
wordlearray = np.zeros((6,5),dtype=str)
wordlecheckarray = np.zeros((6,5),dtype=np.int32)
wordleoftheday = "slate"

def loadwordlist(filename): # load originalwordlist list from json file into a list
    with open(filename) as f:
        originalwordlist = json.load(f)
    return originalwordlist

def updateusedletters(usedwordlist): # log used individual letters
    for word in usedwordlist:
        for letter in word:
            if letter not in usedletters:
                usedletters.append(letter)

def wordlefilter1(word,remainingwordlist): #removeinputword
    remainingwordlist.remove(word)

def inputword():
    word = input("Enter a word: ")
    if word in originalwordlist:
        return word
    else:
        print("Do you really think " +word+ " is a five letter word?")
        return inputword()

originalwordlist = loadwordlist("words.json")
remainingwordlist = originalwordlist
usedwordlist = []
usedletters = []
usedlettersinwordleofthedaywithoutknownposition = []
usedlettersinwordleofthedaywithknownposition = ["","","","",""]
usedlettersnotinwordleoftheday = []

if strategy == 1:
    letters = {} #dictionary of letters and their frequency
    #normalise letter frequency
    for letter in letters:
        letters[letter] = letters[letter]/len(remainingwordlist)

    for word in remainingwordlist: #
        for letter in word:
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1

    #give rank to all words in list according to letter frequency
    remainingwordlist.sort(key=lambda x: sum(letters[l] for l in x))

    #remove words with duplicate letters, run once
    if epoch == 0:
        remainingwordlist = [word for word in remainingwordlist if len(set(word)) == len(word)]
        epoch += 1

# def printsuggestedword(remainingwordlist):
#     #if remainingwordlist empty
#     if len(remainingwordlist) == 0:
#         print("No words left")
#     else:
#         print("Suggested word from strategy 1, phase 1:"+ remainingwordlist[-1])

#suggest word that most likely match word of the day
def strategy1(originalwordlist, remainingwordlist,usedlettersinwordleofthedaywithknownposition, usedlettersinwordleofthedaywithoutknownposition):
    #if remainingwordlist empty
    if len(remainingwordlist) == 0:
        phase = 2
        print("No words left, implement phase 2")
        remainingwordlist = originalwordlist #reset remainingwordlist
    
    filter1(remainingwordlist, usedletters) # remove used letters from word list that contains used letters
    filter2(remainingwordlist, usedlettersinwordleofthedaywithknownposition) # prioritise words that do not contain letters in known positions
    filter3(remainingwordlist, usedlettersnotinwordleoftheday) # remove words that do not contain letters not in wordleoftheday

    return print(remainingwordlist, len(remainingwordlist))

def filter1(remainingwordlist, usedlettersnotinwordleoftheday): # remove words that do not contain letters not in wordleoftheday
    for word in remainingwordlist:
        for usedletter in usedlettersnotinwordleoftheday:
            if usedletter in word:
                try:
                    remainingwordlist.remove(word)
                    print("Removed word by filter 1:", word)
                except:
                    print("Could not remove because word doesn't exist anymore. Phase", phase)


def filter2(remainingwordlist, usedlettersinwordleofthedaywithknownposition): # prioritise words that do not contain letters in known positions
    try:
        length=len(remainingwordlist)
        for word in remainingwordlist:
            for index,letter in enumerate(word): #loop through remaining word letters
                if letter == usedlettersinwordleofthedaywithknownposition[index]:
                    print(index,letter)
                    remainingwordlist.append(remainingwordlist.pop(remainingwordlist.index(word)))
                    print("Popped:", word)
                    break
                else:
                    print("Could not prioritise because word doesn't exist anymore or letter is not in word. Filter 2. Phase", phase)
    except Exception as e:
        print("Problem with the filter: " + e)

def filter3(remainingwordlist,usedlettersnotinwordleoftheday): # remove words that do not contain letters not in wordleoftheday
    try:
        for word in remainingwordlist:
            for index,letter in enumerate(word): #loop through remaining word letters
                if letter in usedlettersnotinwordleoftheday:
                    remainingwordlist.remove(word) #blatantly remove word from list
                    print("Removed word by filter 3:", word)
                    break
                else:
                    print("Could not remove because word doesn't exist anymore or letter is not in word. Filter 3. Phase", phase)
    except Exception as e:
        print("Problem with the filter: " + e)


def getcurrentlayer(usedwordlist):
    return len(usedwordlist)

def fillwordlearraylayer(layer,word):
    for index,letter in enumerate(word): # append letter to wordlearray
        wordlearray[(layer-1),index] = letter

def fillcheckwordlearray(word, layer, wordleoftheday):
    #if letter match wordleoftheday
    for index,letter in enumerate(word): # append 1 to wordlecheckarraylayer
        if letter == wordleoftheday[index]:
            wordlecheckarray[layer-1,index] = 1
            usedlettersinwordleofthedaywithknownposition[index]=letter
        elif letter in wordleoftheday and letter not in usedlettersinwordleofthedaywithoutknownposition: #if letter is in wordleoftheday without known position
            wordlecheckarray[layer-1,index] = 2
            usedlettersinwordleofthedaywithoutknownposition.append(letter)
        else: #letter not in wordleoftheday
            wordlecheckarray[layer-1,index] = 0
            if letter not in usedlettersnotinwordleoftheday:
                usedlettersnotinwordleoftheday.append(letter)

def lose(layer,won):
    if layer == 6 and won == False:
        return True
    else:
        return False

def won(word, wordleoftheday):
    if word == wordleoftheday:
        return True
    else:
        return False
    
    # #sum row of wordlecheckarray
    # checkarrayset =set(wordlecheckarray[layer-1,:])
    # if len(checkarrayset) == 1 and checkarrayset == 1:
    #     return True
    # else:
    #     return False

while True:
    #Strategy 1: 
    #if strategy number 1 is selected, suggest word with highest letter frequency
    if strategy == 1:
        #printsuggestedword(remainingwordlist)
        strategy1(originalwordlist, remainingwordlist, usedlettersinwordleofthedaywithknownposition, usedlettersinwordleofthedaywithoutknownposition)
    
    word = inputword()
    usedwordlist.append(word) #add word to usedwordlist
    layer = getcurrentlayer(usedwordlist)
    fillwordlearraylayer(layer,word)
    fillcheckwordlearray(word, layer, wordleoftheday)
    updateusedletters(usedwordlist) #update usedletters
    wordlefilter1(word,remainingwordlist) #remove used word form remaining list
    
    print("Wordle array", wordlearray)
    print("Wordle check array", wordlecheckarray)
    print("Remaining word count", len(remainingwordlist))
    print("Used word list: ", usedwordlist)
    print("Used letters: ",usedletters)
    print("Used letters not in word of the day: ", usedlettersnotinwordleoftheday)
    print("Used letters in word of the day with known position: ", usedlettersinwordleofthedaywithknownposition)
    print("Used letters in word of the day without known position: ", usedlettersinwordleofthedaywithoutknownposition)
    if won(word, wordleoftheday):
        print("You won!")
        break
    if lose(layer,won(word, wordleoftheday)):
        print("You have lost, too many guesses")
        break