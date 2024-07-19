# create flashcard libraries
# Store data
# Create score
# edit flashcard libraries

import json
import random
import color


def library_empty(x):
    try:
        with open(x, "r") as file:
            data = json.load(file)
            if not data:
                return True
            else:
                return False
    except FileNotFoundError:
        return True
    except json.JSONDecodeError:
        return True


def add():
    title = input("\nwhat would you like to title your new flashcard set? ").lower()
    print(color.blue + title)
    vocab_list = {}
    while True:
        word = input(color.blue + '\nwhat is your word: ')
        meaning = input("what is the meaning to that word: ")
        correct = input("is this correct: " + word + " | " + meaning + " ").lower()

        if correct == "yes":
            vocab_list[word] = meaning
        elif correct == "no":
            continue
        else:
            print(color.red + "error: try again")
            continue

        leave = input(color.blue + 'do you still want to add words: ').lower()

        if leave == 'yes':
            continue
        else:
            print('\n' + title)
            for key, value in vocab_list.items():
                print(color.purple + key + " | " + value)
            new_set = {title: vocab_list.copy()}

            if not library_empty("library.json"):
                with open("library.json", "r") as file:
                    extract = json.load(file)
                extract.update(new_set)

                with open("library.json", "w") as file:
                    json.dump(extract, file)
            else:
                with open("library.json", "w") as file:
                    json.dump(new_set, file)
            break


def view():
    if not library_empty("library.json"):
        with open("library.json", "r") as file:
            l_view = json.load(file)
            for title, hash_v in l_view.items():
                print(color.blue + title)
                for word, definition in hash_v.items():
                    print(color.blue + "word: " + color.white + word + color.blue + " definition: "
                          + color.white + definition)
    else:
        print("study library is empty")


def study():
    if library_empty("library.json"):
        print("error: library is empty")
        return

    with open("library.json", "r") as file:
        entire = json.load(file)
        titles = list(entire.keys())
        titles = "(" + " | ".join(titles) + ")"
    vocab_choice = input("which vocabulary set would you like to study " + color.blue +
                         titles + color.default + ": ").lower()

    if library_empty("library.json"):
        print("error: library is empty. add a new study set")
        return

    with open("library.json", "r") as file:
        entire = json.load(file)

    if vocab_choice in entire:
        current_set = entire[vocab_choice]
        print("let's start studying!")
    else:
        print("error: vocabulary set is not in library")
        return

    key_list = list(current_set.keys())
    print(color.red + "if you answer any question with 'q', you will automatically exit the current study set.")
    score = 0

    while True:
        if score % 5 == 0 and score > 0:
            print(color.white + "\nwow you are on a " + str(score) + " streak!")

        i = random.randint(0, len(current_set) - 1)
        flashcard_question = input(color.blue + "\nword: " + color.white + key_list[i] + color.blue +
                                   " definition: ").lower()
        if flashcard_question == 'q':
            break
        if flashcard_question == current_set[key_list[i]]:
            print("correct")
            score += 1

        else:
            fill_in = ""
            for s in current_set[key_list[i]]:
                fill_in += " _"
            print("wrong\n")
            correction = input("Try again" + color.white + fill_in + color.blue + ": ")
            if correction == current_set[key_list[i]]:
                print("good job. you got it right!")
                score = 1
            else:
                print("you got it wrong again...")
                score = 0
            continue


def edit():
    if library_empty("library.json"):
        print("error: library is empty")
        return

    with open("library.json", "r") as file:
        entire = json.load(file)
        titles = list(entire.keys())
        titles = "(" + " | ".join(titles) + ")"

    edit_choice = input(color.blue + "Select study set that you want to edit " +
                        color.white + titles + color.blue + ": ").lower()

    if edit_choice not in entire:
        print("error: the study set you are looking for is not in study library")
        return
    edit_set = entire[edit_choice]

    while True:
        remove_or_add = input("would you like to remove or add to the set ('q' to exit): ").lower()
        if remove_or_add == 'remove':
            while True:
                print(edit_choice)
                for idx, (curr_word, curr_def) in enumerate(edit_set.items()):
                    print(color.blue + str(idx + 1) + ". word: " + color.white + curr_word + color.blue +
                          " definition: " + color.white + curr_def)
                char_remove = input('which entry would you like to remove (type word): ')

                if char_remove in edit_set:
                    del edit_set[char_remove]
                else:
                    print("error: your entry is not within the study set")
                    continue

                deletion = input("do you want to delete any more terms? ").lower()
                if deletion == 'yes':
                    continue
                else:
                    break

            with open("library.json", "w") as file:
                json.dump(entire, file)

        elif remove_or_add == 'add':
            while True:
                word = input('what is your new word? ')
                definition = input('what is your new definition? ')
                correct = input("is this correct: " + word + " | " + definition + " ").lower()

                if correct == "yes":
                    edit_set.update({word: definition})
                elif correct == "no":
                    continue
                else:
                    print(color.red + "error: try again")
                    continue

                leave = input(color.blue + 'do you still want to add words: ').lower()

                if leave == 'yes':
                    continue
                else:
                    entire[edit_choice] = edit_set
                    with open("library.json", "w") as editFile:
                        json.dump(entire, editFile)
                    print("this is your new set\n" + edit_choice + "\n" + str(edit_set))
                    return

        elif remove_or_add == 'q':
            return
        else:
            print(color.red + "error: try again")
            continue


print(color.default + color.bold + "Welcome to Tony's Flashcards!")

while True:
    option = input(color.default + "\nWould you like to add/view/study/edit? ").lower()

    if option == "add":
        add()
    elif option == "view":
        view()
    elif option == "study":
        study()
    elif option == "edit":
        edit()
    else:
        print("error: try again")
        continue
