#import words.json
import json
from multiprocessing.reduction import duplicate
from timeit import repeat
import numpy as np

with open('words.json') as f:
    allWordleWords = json.load(f)

knownLetters=[]

lettersWithKnownPosition=["","","","",""]

def filterWordsContainingAllKnownLetters(allWordleWords,knownLetters):
    filteredWordleWords=[]
    for word in allWordleWords:
        if all(letter in word for letter in knownLetters):
            filteredWordleWords.append(word)
    return filteredWordleWords




def filterWordsAccordingToKnownPositions(remainingWordleWords,lettersWithKnownPosition):
    if lettersWithKnownPosition == ["","","","",""]:
        return remainingWordleWords
    filteredWordleWords=[]
    for word in remainingWordleWords:
        for index, letter in enumerate(word):
            if letter == lettersWithKnownPosition[index]:
                filteredWordleWords.append(word)
    return filteredWordleWords

remainingWordleWords = filterWordsContainingAllKnownLetters(allWordleWords,knownLetters)
remainingWordleWords = filterWordsAccordingToKnownPositions(remainingWordleWords,lettersWithKnownPosition)
#remainingWordleWords = sortRemainingWordleWordsAccordingToLetterFrequencyAndPosition(remainingWordleWords)

print(remainingWordleWords)



def calculateLetterScoreDict(remainingWordleWords):
    letters={}
    for word in remainingWordleWords:
        letterLevel = getLetterLevel(word)
        for letter in word:
            #if letter in letters and letter not in duplicateLetters:
            if letter in letters:
                letters[letter[letterLevel[letter]]] += 1
            else:
                letters[letter] = 1
    for letter in letters:
        letters[letter] = letters[letter]/len(remainingWordleWords)
    return letters

def getLetterLevel(word):
    "returns a dictionary with count of letters in word as values and letter as key"
    countedRepeatedLetters={}
    for letter in word:
        if letter in countedRepeatedLetters:
            countedRepeatedLetters[letter] += 1
        else:
            countedRepeatedLetters[letter] = 1
    return countedRepeatedLetters

letterScores = calculateLetterScoreDict(remainingWordleWords)

#give score to words according to letter scores
def scoreWords(remainingWordleWords,letterScores):
    wordScores={}
    for word in remainingWordleWords:
        wordScores[word] = sum(letterScores[letter] for letter in word)
    return wordScores

