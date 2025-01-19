from collections import defaultdict
from collections.abc import Set
import regex as re

# Règles du jeu
# Le mot à deviner contient entre 6 et 10 lettres
# La première lettre n'est pas exotique (K, Q, W, X, Y, Z)
# Pas de nom propre
# Pas d'espace, d'apostrophe ou de trait d'union.

WORD_MIN_SIZE = 6
WORD_MAX_SIZE = 10

class sutom_helper(Set):
    def __init__(self, words: set):
        self.words = set() # Dictionnaire complet des mots valides
        self.words_len = defaultdict(set) # Mots rangés par taille        
        self.min_size, self.max_size = (WORD_MIN_SIZE, WORD_MAX_SIZE)

        for word in words:
            wd = word.strip().upper()
            if (len(wd) >= WORD_MIN_SIZE) and (len(wd) <= WORD_MAX_SIZE):
                self.words.add(wd)
                self.words_len[len(word)].add(word)

        self.current_words = self.words 
        self.letters = defaultdict(int) 

    def __contains__(self, value: str):
        wd = value.strip().upper()
        return wd in self.words
    
    def __iter__(self):
        return iter(self.words)
    
    def __len__(self):
        return len(self.words)

    def reset(self):
        self.letters = defaultdict(int)
        self.current_words = self.words

    # information
    def info(self):
        
        return self.current_words
    
    def word_length(self, word_length):
        # Première information : on restreint la recherche en
        # fonction de la longueur du mot à trouver.
        self.current_words = self.words_len[word_length] # liste
        
    def first_letter(self, first_letter):
        # Deuxième information : on restreint la recherche en 
        # fonction de la première lettre du mot à trouver.
        self.current_words = {word for word in self.current_words if word.startswith(first_letter)}
        self.letters[first_letter]+=1

    def last_letter(self, last_letter):
        self.current_words = {word for word in self.current_words if word.endswith(last_letter)}
        self.letters[last_letter]+=1

    def red_letters(self, pattern):
        # pattern est de la forme "A.B..C." où A, B, C sont 
        # les lettres rouges et . sont des emplacements libres
        # TODO: remplacer automatiquement un mauvais formatage :
        # autoriser les patterns avec "-*," etc au lieu de "."
        self.current_words = {word for word in self.current_words if re.match(pattern.upper(), word)}
        for letter in pattern.strip("."):
            self.letters[letter]+=1


    def yellow_letters(self, letters):
        return


    def not_in_word(self, letters):
        for letter in letters:
            self.current_words = {word for word in self.current_words if letter not in word}



