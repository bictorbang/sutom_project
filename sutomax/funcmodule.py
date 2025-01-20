def guesser(helper, choice, manual_guess = ""):
    match choice:
        case "HASARD":
            return helper.guess()
        case "MANUEL":
            return manual_guess
        case "OPTIMAL":
            return "Pas encore implémenté"
        case _:
            return "Erreur !"

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

def first_turn(first_letter, word_length, helper):
    helper.word_length(word_length)
    helper.first_letter(first_letter)
    helper.info()
    return helper.guess()

def next_turn(helper, guess, result):
    helper.new_turn()
    red, yellow, not_there = translate(guess, result)
    helper.red_letters(red)
    helper.yellow_letters(yellow)
    helper.not_in_word(not_there)
    helper.info()
    return helper.guess()

