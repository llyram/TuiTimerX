import random
def genScramble():

    faces = ['R', 'L', 'U', "D", "F", "B"]

    scramble = []

    i = 1

    scramble_length = 20

    while i <= scramble_length:

        rate = 4
        normal = 2
        double = 1 #int(src.settings.read_conf("scramble", "double")) + normal
        prime = 1 #int(src.settings.read_conf("scramble", "prime")) + double

        move = faces[random.randint(0, len(faces) -1)]
        # x = random.randint(0, rate)

        # if x <= normal:
        #     add = ""
        # elif normal < x <= double:
        #     add = "2"
        # elif double < x <= prime:
        #     add = "\'"

        add = random.choice(["", "2", "\'"])

        if len(scramble) == 0:
            scramble.append(str(move) + add)
            i = i+1

        if not move == scramble[len(scramble)-1][0]:
            scramble.append(str(move) + add)
            i = i+1
    return " ".join(scramble)