# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Valerii Sdobnikov
# Time spent    : 1.5h

import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

#region
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
#endregion

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):

    word = word.replace(' ', '').lower()

    sum = 0
    for char in word:
        if char == '*': continue
        sum += SCRABBLE_LETTER_VALUES[char]

    wordlen = len(word)

    return max(1, 7*wordlen - 3*(n-wordlen)) * sum

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for _ in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for _ in range(num_vowels, n-1):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand['*'] = 1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):

    new_hand = dict()
    word = word.lower()
    for char in hand.keys():

        count = hand[char] - word.count(char)

        if count <= 0: continue
        new_hand[char] = count

    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):

    word = word.lower()

    result = True

    for i in set(word):

        if i not in hand.keys():
            result = False
            continue

        result &= hand[i] >= word.count(i)

    result2 = False
    if '*' in word:
        possible = [word.replace('*', i) for i in VOWELS]

        for i in possible:
            result2 |= i in word_list

    else:
        result2 = word in word_list

    return result & result2


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):

    return sum(hand.values())

def play_hand(hand, word_list):
    
    total_score = 0
    while calculate_handlen(hand) >= 1:

        print("Current hand: ", end='')
        display_hand(hand)

        inp = input('Enter word, or “!!” to indicate that you are finished: ').replace(' ', '').lower()

        if inp == '!!': break

        if is_valid_word(inp, hand, word_list):
            score = get_word_score(inp, calculate_handlen(update_hand(hand, inp)))

            total_score += score
            print(f'“{inp}” earned {score} points. Total: {total_score} points')

        else:
            print('This is not a valid word. Please choose another word.')

        hand = update_hand(hand, inp)
    reason = 'Ran out of letters.\n' if calculate_handlen(hand) <= 0 else ''
    print(reason + f'Total score for this hand: {total_score}')
    print('--------')

    return total_score


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    
    if len(letter) != 0 or not (letter in VOWELS or letter in CONSONANTS): return hand

    if not letter in hand.keys():
        return hand

    lst = []

    if letter in VOWELS:
        lst = list(set(VOWELS) - set(letter))

    else:
        lst = list(set(CONSONANTS) - set(letter))

    new_letter = random.choice(lst)

    new_hand = dict()

    for key, value in hand.items():
        if letter == key:
            new_hand[new_letter] = value
            continue
        new_hand[key] = value

    return new_hand
    

def get_uint(msg):
    while True:
        inp = input(msg)
        try: 
            val = int(inp)
            if not val > 0:
                print('Number must be greater than zero.')
                continue
            return val
        except:
            print('Please enter correct number.')


    
def play_game(word_list):

    print()
    
    total_score = 0
    num_of_hands = get_uint('Enter total number of hands: ')

    hand_replayed = False

    for _ in range(num_of_hands):
        hand = deal_hand(HAND_SIZE)
        print('Current hand: ', end='')
        display_hand(hand)

        inp = input('Would you like to substitute a letter? ').lower().replace(' ', '')
        
        if inp == 'yes':
            a = input('Which letter would you like to replace: ').lower().replace(' ', '')
        
            if a in VOWELS + CONSONANTS:
                hand = substitute_hand(hand, a)
            
            print('Current hand: ', end='')
            display_hand(hand)

        print()
        score = play_hand(hand, word_list)
        replay_score = 0
        if not hand_replayed:
            inp2 = input('Would you like to replay the hand? ').replace(' ', '').lower()

            if inp2 == 'yes':
                replay_score = play_hand(hand, word_list)

        total_score += max(score, replay_score)

    print('--------')
    print(f'Total score over all hands: {total_score}') 

 
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
