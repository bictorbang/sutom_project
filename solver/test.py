from collections import defaultdict
from sutomax.classmodule import sutom_helper
from sutomax.funcmodule import translate, valid_pool

# Simuler des parties de Sutom. 

FIRST_LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "L", "M", "N",
                 "O", "P", "R", "S", "T", "U", "V"]


def get_result(target, guess):
    # Donne le résultat de la tentative.
    # Exemple - mot à deviner (helper.target) : "MAESTRO", tentative (guess) : "MAOUSSE"
    # Renvoie "RRJ.J.J"
    result = ""
    red_idx = []
    # La première boucle détecte les lettres ROUGES.
    for idx, (l_target, l_guess) in enumerate(zip(target, guess)):
        if l_target == l_guess:
            result += "R"
            red_idx.append(idx) # on garde en mémoire les indices des lettres ROUGES
        else: 
            result += "."

    # result est de la forme "RR.....". On va désormais rajouter les lettres JAUNES.
    
    yellow_guess = [ch for i, ch in enumerate(guess) if i not in red_idx]
    yellow_target = [ch for i, ch in enumerate(target) if i not in red_idx]

    for idx, l_guess in enumerate(guess):
        if l_guess in yellow_guess:             # Si la lettre n'est pas rouge...
            if l_guess in yellow_target:        # et que la lettre est présente... 
                result = list(result)
                result[idx] = "J"               # obligé de convertir en liste pour des raisons de typage.
                result = ''.join(result)
                yellow_target.remove(l_guess)
            else:                               # Sinon, on ne fait rien
                pass

    return result

def is_solution(result):
    return all(flag == "R" for flag in result)

def solver(helper):  
    logs = []
    target = helper.get_target()
    helper.word_length(len(target)) # Initialisation
    helper.first_letter(target[0])  # Initialisation
    while len(helper) > 0:
        helper.new_turn()
        guess = helper.random_guess()
        logs.append(guess)
        result = get_result(target, guess)
        if is_solution(result): return len(logs), logs
        red, yellow, not_there = translate(guess, result)
        helper.red_letters(red)
        helper.yellow_letters(yellow)
        helper.not_in_word(not_there)
        if len(logs) > 6: break # Prévention contre boucle infini (au cas où)
        # TODO: c'est un peu moche là
    if len(logs) > 6 or guess != helper.target: 
        return 100000, logs


    

def test_random_guess_fixed_len(word_len, n_random = 100):
    # word_len fixe la longueur des mots.
    # On teste n_random fois chaque partie pour moyenner le nombre de coups requis.
    helper = sutom_helper.load_words()
    helper.word_length(word_len)
    words = helper.get_current_words()
    avg_tries_total = defaultdict()
    for letter in FIRST_LETTERS:
        avg_tries_total[letter] = 0
        for word in words:
            helper.set_target(word)
            tries_total = []
            avg_tries = 0
            for _ in range(n_random):
                helper.reset()
                tries, _ = solver(helper)
                tries_total.append(tries)
            




def test_random_guess(n_random = 10):
    #TODO: c'est trop long. Il faut optimiser le temps. Il y a trop de latence 
    helper = sutom_helper.load_words()
    words = helper.get_current_words()
    avg_tries_list = []
    for idx, word in enumerate(words):
        if idx%10 == 1: 
            print(f"Test numéro {idx}")
            current_avg = sum(avg_tries_list) / len(avg_tries_list)
            print(f"Moyenne actuelle de tentatives : {current_avg}")

        tries_total = []
        for _ in range(n_random):
            helper.reset()
            helper.set_target(word)
            tries, _ = solver(helper)
            tries_total.append(tries)
        avg_tries_list.append(sum(tries_total) / n_random)
    return sum(avg_tries_list) / len(avg_tries_list)


    
target = "MAESTRO"
guess = "MAOUSSE"

print(get_result(target, guess))

helper = sutom_helper.load_words()
helper.set_target("MAESTRO")
print(solver(helper))

print(test_random_guess())