import math

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
    def setRank(self, rank):
        self.rank = rank
    def setSuit(self, suit):
        self.suit = suit
    def getRank(self):
        return self.rank
    def getSuit(self):
        return self.suit

#hand is a list of integers
def pairs(hand):
    total = 0
    for x in range(len(hand) - 1):
        for y in range(x + 1, len(hand)):
            if (hand[x] == hand[y]):
                total += 2
    return total

#measures sum of a set of cards by converting face card values to 10, where combo is a list of integers
def faceValue(combo):
    sum = 0
    for rank in combo:
        if (rank > 10):
            sum += 10
        else:
            sum += rank
    return sum

#combinations a list of integer lists (representing all possible combinations of a set of cards)
def fifteens(combinations):
    total = 0
    for comb in combinations:
        if faceValue(comb) == 15:
            total += 2
    return total

#combo is a list of integers, returns whether it represents a run by measuring distance of each element from the average
def isRun(combo):
    length = len(combo)
    avg = sum(combo) / length
    nums = []
    for rank in combo:
        distance = abs(rank - avg)
        if(distance > 0.5 * length - 0.5):
            return False
        #checks for duplicate values
        if (nums.count(rank) > 0):
            return False
        nums.append(rank)
    return True

#combinations a list of integer lists (representing all possible combinations of a set of cards)
def runs(combinations):
    total = 0
    maxLen = 3
    potentialRuns = []
    for combo in combinations:
        #runs must be of length 3 or greater
        length = len(combo)
        if(length >= maxLen and isRun(combo)):
            potentialRuns.append(combo)
            if(length > maxLen):
                maxLen = length  
    for run in potentialRuns:
        if (len(run) == maxLen):
            total += maxLen
    return total

#generates all possible combinations of all lengths from give list of integers
def allcombinations(hand):
    combinations = [[]]
    for rank in hand:
        for set in combinations.copy():
            combinations.append(set + [rank])
    return combinations

#calculates 'dry' score of hand, strictly based on card ranks (excludes flushes and nobs)
#hand is an unsorted list of 5 integers representing card ranks ex. [3, 4, 8, 7, 4]
def dryScore(handRanks):
    combos = allcombinations(handRanks)
    return pairs(handRanks) + fifteens(combos) + runs(combos)

def fnSuits(cards):
    suits = [[], []]
    flushsuit = cards[0].getSuit()
    for card in cards:
        if card.getRank() == 11:
            suits[0].append(card.getSuit())
        if card.getSuit() != flushsuit:
            flushsuit = -1
    if flushsuit >= 0:
        suits[1].append(flushsuit)
    return suits

#fn is list of lists, returns whether fn contains val in any of its lists
def inLists(val, listoflists):
    for l in listoflists:
        if val in l:
            return True
    return False

def nobs(cards, blockers, fn):
    if not fn: return 0
    return (len(fn) * 13 - blockers) / 46

def flush(cards, blockers, fn):
    if not fn: return 0
    score = 1
    for x in range(5 - len(cards)):
        score *= (len(fn) * 13 - blockers - x) / (46 - x)
    if len(cards) == 4:
        score += 4
    return score

#cards and remainingknowns are lists of Card objects
def wetScore(cards, remainingknowns):
    score = 0
    fn = fnSuits(cards)
    if fn:
        blockers = 0
        for card in cards + remainingknowns:
            if inLists(card.getSuit(), fn):
                blockers += 1
        score += nobs(cards, blockers, fn[0]) + flush(cards, blockers, fn[1])
    return score


#hand is an list of Card objects, representing a starting hand of six cards
#returns dict representing full deck of cards minus the ones in the starting hand
def remainingCards(hand):
    deck = {}
    for rank in range(13):
        deck[rank + 1] = 4
    for card in hand:
        deck[card.getRank()] -= 1    
    return deck

# generates all combinations of size length from set, returns in list form
# no rep specifies whether combinations should allow repetition
def combinations(set, length, norep, prev = []):
    combos = []
    if len(prev) == length:
        return [prev]
    for index, rank in enumerate(set):
        cprev = prev.copy()
        cprev.append(rank)
        combos += combinations(set[index + norep:], length, norep, cprev)
    return combos

#for each integer r in rlist, lists possible combinations (with repetition) in tuple ranks of size r, then concatenates each individual combo list 
#ex. ranks = (2, 4), rlist = [1, 2]
#returns: [[2, 2, 2], [2, 2, 4], [2, 4, 4], [4, 2, 2], [4, 2, 4], [4, 4, 4]]
def joinCombos(ranks, rlist):
    norep = False
    combos = []
    if len(rlist) == 1:
        return combinations(ranks, rlist[0], norep)
    for combo1 in joinCombos(ranks, rlist[0: len(rlist) - 1]):
        for combo2 in combinations(ranks, rlist[len(rlist) - 1], norep):
            combos.append(combo1 + combo2)
    return combos

#takes a list of elements, returns number of permutations, list may have repeating elements
def permutations(multiset):
    num = math.factorial(len(multiset))
    counts = {}
    for elem in multiset:
        if elem in counts:
            counts.update({elem: counts.get(elem) + 1})
        else:
            counts.update({elem : 1})
    for type in counts:
        num *= 1 / math.factorial(counts.get(type))
    return num

#splits combo into sublists based on the sublist lengths specified in format, finds the number of permutations of each sublist,
#returns product of all of these permutations
#ex. combo = [1, 1, 2, 2], format = [1, 2], splits combo into [1] and [1, 2, 2], returns 1*3 = 3
def numArrangements(combo, format):
    arrangements = 1
    for length in format:
        arrangements *= permutations(combo[0:length])
        combo = combo[length:]
    return arrangements

#deck is a dict of key-value pairs, returns how many cards it represents
def deckSize(deck):
    amount = 0
    for card in deck:
        amount += deck.get(card)
    return amount

#takes list of ints returns product of all items in the list
def product(ints):
    product = 1
    for num in ints:
        product *= num
    return product

#takes list of card objects returns list representing ranks of those cards
def toRanks(cards):
    ranks = []
    for card in cards:
        ranks.append(card.getRank())
    return ranks

# calculates the expected score of a given
def score(kept, tocrib, isDealer):
    ranks = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    #dict reprsenting the remaining frequency of each suit in the deck once the starting hand has been dealt
    remaining = remainingCards(kept + tocrib) 
    #determines whether cards sent to the crib count for or against the player, based on whether the player is the dealer
    cribMultiplier = -1
    if isDealer:
        cribMultiplier = 1
    
    #calculates suit-based value of crib and kept cards (ie. flush and nobs)
    cribscore = cribMultiplier * wetScore(tocrib, kept)
    keptscore = wetScore(kept, tocrib)
    
    #lists possible combinations of one starter cards and two cards opponent sends to crib
    format = [1, 2]
    posscombos = joinCombos(ranks, format)
    
    #calculate expected dry score of 2 cards player sends to crib
    for combo in posscombos:
        cremaining = remaining.copy()
        prob = []
        arrangements = numArrangements(combo, format)
        for i, rank in enumerate(combo):
            scarcity = cremaining[rank]
            cremaining[rank] = scarcity - 1
            prob.append(scarcity / (deckSize(remaining) - i))
        cribscore += cribMultiplier * (dryScore(toRanks(tocrib) + combo) * product(prob) * arrangements)

    #calculate expected dry score of 4 cards that are kept
    for rank in ranks:
        prob = remaining.get(rank) / deckSize(remaining)
        keptscore += dryScore(toRanks(kept) + [rank]) * prob
    return cribscore + keptscore

#takes a list of integer tuples represnting cards, converts to a list of Card objects
def toCardList(tuples):
    cards = []
    for card in tuples:
        cards.append(Card(card[0], card[1]))
    return cards

#inverse of toCardList, takes list of Card objects and converts to a list of integer tuples
def toTuples(clist):
    ctups = []
    for card in clist:
        ctups.append((card.getRank(), card.getSuit()))
    return ctups

#takes a list of tuples, merge sorts by third value of each tuple (in this case is always the combination's score)
#ex. ((((1, 2), (3, 1), (12, 0), (6, 2)), ((4, 2), (1, 1)), 10.8762), ... )
def sorted(tups):
    if len(tups) == 1:
        return tups
    first = sorted(tups[0: len(tups) // 2])
    second = sorted(tups[len(tups) // 2: ])
    # join two sorted lists
    i = 0
    for elem in first:
        while i < len(second) and elem[2] < second[i][2] :
            i += 1
        second.insert(i, elem)
    return second

def scoreList(handList, isDealer):
    #Sample input:
    #handList = [(2, 0), (2, 2), (4, 2), (4, 3), (10, 3), (4, 3)]
    #isDealer = True

    startingHand = toCardList(handList)
    scores = []

    #Generate all possible four card combinations from starting hand
    #Iterate over these combinations:
    for combo in combinations(startingHand, 4, True):
        #each tuple represents (kept cards, cards sent to crib, score of combination)
        scores.append((toTuples(combo), toTuples(list(set(startingHand) - set(combo))), score(combo, list(set(startingHand) - set(combo)), isDealer)))
    return sorted(scores)
