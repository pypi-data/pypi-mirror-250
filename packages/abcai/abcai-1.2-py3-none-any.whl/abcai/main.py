import os


def list():
    lists = [
        "alpha_beta_pruning.py",
        "A_star.py",
        "BFS(breath).py",
        "cryto_arthrmatic.py",
        "DFS(depth).py",
        "expert_system.py",
        "min_max.py",
        "Naive_Bayes.py",
        "NLP_token.py",
        "predicate-logic.py",
        "sematic_net.py",
        "spell_check.py",
    ]
    for num, i in enumerate(lists):
        print(num + 1, i)


def run():
    list()

    ch = int(input("enter the choice"))

    if ch == 1:
        with open("BFS(breath).py", "r") as info:
            con = info.read()

            print(con)
            print("Done 🔥")

    if ch == 2:
        with open("A_star.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 3:
        with open("DFS(depth).py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 4:
        with open("alpha_beta_pruning.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 5:
        with open("cryto_arthrmatic.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 6:
        with open("expert_system.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 7:
        with open("min_max.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 8:
        with open("Naive_Bayes.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 9:
        with open("NLP_token.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 10:
        with open("predicate-logic.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 11:
        with open("sematic_net.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    if ch == 12:
        with open("spell_check.py", "r") as info:
            con = info.read()
            print(con)
            print("Done 🔥")

    print("Done 🔥")
