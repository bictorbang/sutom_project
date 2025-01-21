import click 
import regex as re

GUESSER_WORDS = {
    1: ["1", "&", "GUESS", "HASARD", "RANDOM", "R"],
    2: ["2", "é", "MANUEL", "MANUAL", "M"],
    3: ["3", '"', "OPTIMAL", "O"],
    4: ["4", "'", "ABANDON", "Q"],
    5: ["5", "(", "INFO", "INFORMATIONS", "INFORMATION", "HELP", "H", "I"]
}

RESULT_WORDS = {
    1: ["1", "RETOUR", "AUTRE", "A", "B", "BACK", "OTHER", "R"],
    2: ["2", "GAGNÉ", "GAGNE", "TERMINÉ", "TERMINE", "TROUVÉ", "TROUVE", "OK", "Q", "T", "G", "Y"]
}

def lookup_words(word, lookup):
    for l in lookup.values():
        if word in l:
            return list(lookup.keys())[list(lookup.values()).index(l)]

def valid_first_letter(letter):
    return re.search(f'^[A-Z]$', letter) and re.search(f'^[^KQWXYZ]$', letter)

def valid_length(length):
    return length <= 10 and length >= 6

def valid_word(word, helper):
    return len(word) == helper.current_word_len and word[0] == helper.current_word_first

def valid_result(result, helper):
    return len(result) == helper.current_word_len and re.search(f'^[.RJ]*$', result)

def valid_pool(helper):
    return len(helper) > 0

def guesser(helper, choice):
    match choice:
        case 1:
            random_guess = helper.random_guess()
            click.echo(f'Essayez{random_guess} !')
            return random_guess
        case 2:
            manual_guess = click.prompt('Inscrivez le mot choisi ').upper()
            while not valid_word(manual_guess, helper):
                manual_guess = click.prompt('Veuillez rentrer un mot valide.').upper()
            click.echo(f'Essayez {manual_guess} !')
            return manual_guess
        case 3:
            print("Pas encore implémenté")
        case _:
            return "Erreur !"

def info_turn(helper):
    pass

def user_turn(helper):
    choice = click.prompt('Que faire ? \nHasard [1]    Manuel [2]    Optimal [3]    Abandon [4]    Info [5] ').upper()
    choice = lookup_words(choice, GUESSER_WORDS)
    if not choice:
        click.echo("Veuillez retourner une réponse valide.")
        return user_turn(helper)
    if choice == 4:
        click.echo('Dommage. Une prochaine fois ! :)')
        return None, None
    if choice == 5: 
        info_turn(helper)
        return user_turn(helper)
    guess = guesser(helper, choice) 
    result = click.prompt('Alors ? (RETOUR [1] pour un autre choix, TROUVÉ [2] pour terminer)', type = str).upper()
    result_temp = lookup_words(result, RESULT_WORDS)
    if not result_temp:
        while not valid_result(result, helper):
            result = click.prompt('Veuillez rentrer un résultat valide. (R pour rouge, J pour jaune, . pour le reste)', type = str).upper()
        return guess, result
    elif result_temp == 1:
        return user_turn(helper)
    else: #elif result_temp == 2:
        click.echo(f"Félicitations, vous avez trouvé le mot ! Solution : {guess}")
        return None, None

def translate(guess, result):
    red = ""
    yellow = ""
    not_there = ""

    for letter, flag in zip(guess, result):
        if flag == "R":
            red += letter
            yellow += "."
        elif flag == "J":
            red += "."
            yellow += letter
        else:
            red += "."
            yellow += "."
            not_there += letter
    
    return red, yellow, not_there

def first_turn(helper):
    first_letter = click.prompt('Première lettre du mot ', type = str).upper()
    while not valid_first_letter(first_letter):
        first_letter = click.prompt('Veuillez entrer une lettre valide. (A à Z sauf K, Q, W, X, Y, Z)', type = str).upper()
    word_length = click.prompt('Longueur du mot ', type = int)
    while not valid_length(word_length):
        word_length = click.prompt('Veuillez entrer une longueur valide. (Entre 6 et 10)', type = int)
    helper.word_length(word_length)
    helper.first_letter(first_letter)
    helper.info()
    guess, result = user_turn(helper)
    return guess, result

def next_turn(helper, guess, result):
    helper.new_turn()
    red, yellow, not_there = translate(guess, result)
    helper.red_letters(red)
    helper.yellow_letters(yellow)
    helper.not_in_word(not_there)
    if not valid_pool(helper):
        click.echo('OK il y a eu une douille !') #TODO: annuler le changement. Il faut l'état du tour précédent en mémoire
    helper.info()
    guess, result = user_turn(helper)
    return guess, result

def endgame():
    return click.confirm("Voulez-vous rejouer ?")
    