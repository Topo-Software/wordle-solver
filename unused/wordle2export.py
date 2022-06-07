# %%
knownLetters=split("retv")#all yellow or green
usedLetters=np.array(split("rebustigerfixerfinerliver")) #all used letters
usedLettersWithUnknownPosition= [["r","t"],["e"],["v"],[],[]] #only yellow used letters in correct position
lettersWithKnownPosition=["","","","e","r"]#green

# %%
#import words.json
import json
import numpy as np
from string import ascii_lowercase as alphabet

with open('newWords.json') as f:
    allWordleWords = json.load(f)

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
        allConditionsMet=False
        for index, letter in enumerate(word):
            if lettersWithKnownPosition[index]=="":
                pass
            elif letter in lettersWithKnownPosition[index]:
                allConditionsMet=True
            else:
                allConditionsMet=False
        if allConditionsMet:
            filteredWordleWords.append(word)
    return filteredWordleWords

def filterWordsAccordingToAvailableLetters(remainingWordleWords,availableLetters):
    filteredWordleWords=[]
    for word in remainingWordleWords:
        if all(letter in availableLetters for letter in word):
            filteredWordleWords.append(word)
    return filteredWordleWords





def filterWordsAccordingToKnownLetterPositions(remainingWordleWords,availableLettersWithPosition):
    filteredWordleWords=[]
    
    for word in remainingWordleWords:
        allLettersAvailable=True
        for index, letter in enumerate(word):
            if letter not in availableLettersWithPosition[index]:
                allLettersAvailable=False
        if allLettersAvailable:
            filteredWordleWords.append(word)
    return filteredWordleWords

#determine unique letters that cannot be in word
def getAvailableLetters(knownLetters,usedLetters):
    availableLetters=[]
    for letter in alphabet:
        if letter in knownLetters or letter not in usedLetters:
            availableLetters.append(letter)
    return availableLetters

def availableLettersAccordingToPosition(usedLettersWithUnknownPosition):
    availableLetters=[[],[],[],[],[]]
    for letter in alphabet:
        for index, usedLetterArray in enumerate(usedLettersWithUnknownPosition):
            if letter not in usedLetterArray:
                availableLetters[index].append(letter)
    return availableLetters

def split(word):
    return [char for char in word]


# %%
availableLettersWithPosition = availableLettersAccordingToPosition(usedLettersWithUnknownPosition)
availableLetters = getAvailableLetters(knownLetters,usedLetters)
remainingWordleWords = filterWordsContainingAllKnownLetters(allWordleWords,knownLetters)
remainingWordleWords = filterWordsAccordingToKnownPositions(remainingWordleWords,lettersWithKnownPosition)
remainingWordleWords = filterWordsAccordingToAvailableLetters(remainingWordleWords,availableLetters)
remainingWordleWords = filterWordsAccordingToKnownLetterPositions(remainingWordleWords,availableLettersWithPosition)

# %%
letterCountDict = {}
for letter in alphabet:
    letterCountDict[letter] = [0,0,0,0,0]

# %%
for word in remainingWordleWords:
    for index, letter in enumerate(word):
        letterCountDict[letter][index] += 1

# %%
normalizedLetterCountDict = {}
for letter in alphabet:
    normalizedLetterCountDict[letter] = [0,0,0,0,0]
    for index, count in enumerate(letterCountDict[letter]):
        normalizedLetterCountDict[letter][index] = count/len(remainingWordleWords)


# %%
#determine probability duplicate letters in remaining word list index is letter number of occurrences
letterMultiplesArray = {}
for letter in alphabet:
    letterMultiplesArray[letter] = [0,0,0,0,0]

# %%
for word in remainingWordleWords:
    for letter in word:
        letterMultiplesArray[letter][word.count(letter)-1] += 1

# %%
# normalise letterMultiplesArray
normalizedLetterMultiplesDict = {}
for letter in alphabet:
    normalizedLetterMultiplesDict[letter] = [0,0,0,0,0]
    for index, count in enumerate(letterMultiplesArray[letter]):
        normalizedLetterMultiplesDict[letter][index] = count/len(remainingWordleWords)

# %%
#rate all words in remainingWordleWords return dictionary with word as key and score as value
wordScoreDict = {}
for word in remainingWordleWords:
    score = 0
    for index, letter in enumerate(word):
        score += normalizedLetterCountDict[letter][index]
    
    wordScoreDict[word] = score

# %%
#rate all words according to multiple of letter
wordScoreMultipleDict = {}
for word in remainingWordleWords:
    score = 0
    for index, letter in enumerate(word):
        score += normalizedLetterMultiplesDict[letter][index]
    
    wordScoreMultipleDict[word] = score

# %%
#sort wordScoreDict by value
sortedWordScoreDict = sorted(wordScoreDict.items(), key=lambda x: x[1], reverse=True)
print(sortedWordScoreDict)

# %%
sortedWordScoreMultipleDict = sorted(wordScoreMultipleDict.items(), key=lambda x: x[1], reverse=True)
print(sortedWordScoreMultipleDict)

# %%
totalScoreDict = {}
for word in remainingWordleWords:
    for index, letter in enumerate(word):
        #count letter in word
        multiple=word.count(letter)
        totalScoreDict[word] = normalizedLetterCountDict[letter][index] + normalizedLetterMultiplesDict[letter][multiple]

# %%
#sort totalScoreDict by value
sortedTotalScoreDict = sorted(totalScoreDict.items(), key=lambda x: x[1], reverse=True)
print(sortedTotalScoreDict)

# %%
# #remainingWordleWords = sortRemainingWordleWordsAccordingToLetterFrequencyAndPosition(remainingWordleWords)
# def calculateLetterScoreDict(remainingWordleWords):
#     letters={}
#     for word in remainingWordleWords:
#         letterLevel = getLetterLevel(word)
#         for index, letter in enumerate(word):
#             #if letter in letters and letter not in duplicateLetters:
#             if letter in letters:
#                 letters[letter] = letterFrequencyArray(letter,letterLevel)
#             else:
#                 letters[letter] = 1
#     # for letter in letters:
#     #     letters[letter] = letters[letter]/len(remainingWordleWords)
#     return letters

# def letterFrequencyArray(letter,letterLevel):
#     "returns the frequency of letter in word in an array of five elements"
#     letterCount = letterLevel[letter]
#     for position in range(letterCount):
#         letterFrequencyArray[position] += 1
#     return letterFrequencyArray

# def getLetterLevel(word):
#     "returns a dictionary with count of letters in word as values and letter as key"
#     countedRepeatedLetters={}
#     for letter in word:
#         if letter in countedRepeatedLetters:
#             countedRepeatedLetters[letter] += 1
#         else:
#             countedRepeatedLetters[letter] = 1
#     return countedRepeatedLetters



# #give score to words according to letter scores
# def scoreWords(remainingWordleWords,letterScores):
#     wordScores={}
#     for word in remainingWordleWords:
#         wordScores[word] = sum(letterScores[letter] for letter in word)
#     return wordScores

# letterScores = calculateLetterScoreDict(remainingWordleWords)

# %%



