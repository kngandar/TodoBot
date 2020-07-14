# -- Class --
class User:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

        self.todo = []
        self.done_todo = []
        self.prize = []
        self.done_prize = []


class Bullet:
    def __init__(self, text, exp):
        self.text = text
        self.exp = exp


# -- Functions --

def load_data(file, user_data):
    with open(file, 'r') as f:
        lines = [line.rstrip() for line in f]

    for x in lines:
        data = x.split(",")
        print(data)
        human = User(data[0], int(data[1]))
        user_data.append(human)

    print('Loaded data~~')

    f.close()


def save_data(file, user_data):
    with open(file, 'w') as f:
        for user in user_data:
            f.write(user.name + "," + str(user.exp) + "\n")

    print('Saved data~~')

    f.close()


def parse_message(text):
    # Parse message into entries and exp pts associated
    text_list = text.split(', ')
    text_list.sort()

    bullet_list = []

    for x in text_list:
        i = x.find('(')
        points = int(x[i+1:-1])
        bullet_list.append(Bullet(x, points))

    return bullet_list
