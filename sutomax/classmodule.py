from collections import defaultdict
from collections.abc import Set
import regex as re
import random

# Règles du jeu
# Le mot à deviner contient entre 6 et 10 lettres
# La première lettre n'est pas exotique (K, Q, W, X, Y, Z)
# Pas de nom propre
# Pas d'espace, d'apostrophe ou de trait d'union.

WORD_MIN_SIZE = 6
WORD_MAX_SIZE = 10
WORD_FILE = "data/listeMotsProposables.ts"

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

        self.current_word_len = 0
        self.current_word_first = ""
        self.current_words = self.words 
        self.letters = defaultdict(int) 
    
    @classmethod
    def load_words(helper, file_name = WORD_FILE, sep = " "):
        words = set()
        with open(file_name, encoding="utf-8", mode="r") as f:
            for line in f.readlines()[2:-2]:
                words.add(line.strip().split(",")[0][1:-1])
        return helper(words)

    def __contains__(self, value: str):
        wd = value.strip().upper()
        return wd in self.current_words
    
    def __iter__(self):
        return iter(self.current_words)
    
    def __len__(self):
        return len(self.current_words)

    def reset(self):
        self.letters = defaultdict(int)
        self.current_words = self.words
        self.current_word_len = 0
        self.current_word_first = ""

    def new_turn(self):
        self.letters = defaultdict(int)

    # information
    def info(self):
        print(f"Il y a {len(self.current_words)} mot(s) correspondant(s).")
        return len(self.current_words)
    
    def random_guess(self):
        word = random.choice(list(self.current_words))
        print(f"Essayez {word} !")
        return word
    
    def word_length(self, word_length):
        # Première information : on restreint la recherche en
        # fonction de la longueur du mot à trouver.
        self.current_words = self.words_len[word_length] # liste
        self.current_word_len = word_length
        
    def first_letter(self, first_letter):
        # Deuxième information : on restreint la recherche en 
        # fonction de la première lettre du mot à trouver.
        self.current_words = {word for word in self.current_words if word.startswith(first_letter)}
        self.letters[first_letter]+=1
        self.current_word_first = first_letter
    '''
    def last_letter(self, last_letter):
        self.current_words = {word for word in self.current_words if word.endswith(last_letter)}
        self.letters[last_letter]+=1
    '''

    def red_letters(self, pattern):
        # pattern est de la forme "A.B..C." où A, B, C sont 
        # les lettres rouges et . sont des emplacements libres
        # TODO: remplacer automatiquement un mauvais formatage :
        # autoriser les patterns avec "-*," etc au lieu de "."
        for letter in pattern.strip("."):
            self.letters[letter]+=1
        self.current_words = {word for word in self.current_words if re.match(pattern.upper(), word)}



    def yellow_letters(self, pattern):
        # pattern est de la forme "..D.E..E" où D, E sont 
        # des lettres jaunes. On ignore les lettres rouges mais 
        # attention à l'emplacement des lettres jaunes !
        # TODO: de même que pour red_letters().
        for letter in pattern.replace(".", ""):
            self.letters[letter]+=1
        # assure que les lettres jaunes sont présentes dans le mot
        self.current_words = {word for word in self.current_words if set(pattern.replace('.', '')) <= set(word)} 
        # assure que les lettres jaunes sont dans une autre position !       
        pattern = re.sub("([A-Z])", r"[^\1]", pattern.upper())
        self.current_words = {word for word in self.current_words if re.match(pattern, word)}
        

    def not_in_word(self, letters):
        for letter in letters:
            if letter not in self.letters:
                self.current_words = {word for word in self.current_words if letter not in word}
            else:
                count = self.letters[letter]
                pattern = f"^([^{letter}]*{letter}[^{letter}]*){{{count}}}$"
                self.current_words = {word for word in self.current_words if re.match(pattern, word)}



