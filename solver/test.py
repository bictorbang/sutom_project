from sutomax.classmodule import sutom_helper
from sutomax.funcmodule import solver

import time

# Simuler des parties de Sutom. 
   

def test_random_guess(target, n_random = 100, verbose = True):
    # word_len fixe la longueur des mots.
    # On teste n_random fois chaque partie pour moyenner le nombre de coups requis.
    timer = time.time()
    helper = sutom_helper.load_words()
    avg_score = 0
    scores = []
    outliers = []
    for _ in range(n_random):
        helper.reset()
        helper.set_target(target)
        tries, logs = solver(helper)
        if tries > 6: 
            outliers.append(logs)
        scores.append(tries)
    avg_score = sum(scores) / len(scores)  
    if verbose: 
        print(f"Cible : {target},   avg_score = {avg_score},    outliers = {outliers}")  
        print((f"Temps écoulé : {time.time() - timer:.3}s"))   
    return avg_score, outliers     

def test_random_guess_all(n_random = 10):
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
    
#target = "MAESTRO"
#guess = "MAOUSSE"
#print(get_result(target, guess))

test_random_guess("BOYARD")
