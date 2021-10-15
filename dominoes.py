from random import shuffle, randint

max_dots = 6
tpp = 7  # tiles per player

computer, player, stock, snake = [], [], [], []
status = ''


def calculate_max_double_per_player(part):
    part_doubles = [item for item in part if item[0] == item[1]]
    if not part_doubles:
        return []
    return max(part_doubles)


def init():
    domino = [[i, j] for i in range(max_dots + 1) for j in range(i, max_dots + 1)]
    shuffle(domino)
    #  computer, player = [domino.pop() for _ in range(7)], [domino.pop() for _ in range(7)]
    return domino[:tpp], domino[tpp:2 * tpp], domino[2 * tpp:]


def print_interface():
    print("=" * 70)
    print("Stock size:", len(stock))
    print("Computer pieces:", len(computer))
    print()
    print_snake()
    print()
    print("Your pieces:")
    for index, piece in enumerate(player, 1):
        print(index, piece, sep=":")
    print()
    print(f"Status: {check_status()}")


def print_snake():
    if len(snake) <= 6:
        for piece in snake:
            print(piece, end="")
        print()
    else:
        for i in range(3):
            print(snake[i], end="")
        print("...", end="")
        for i in range(len(snake) - 3, len(snake)):
            print(snake[i], end="")
        print()


def check_status():
    if status == 'computer':
        return "Computer is about to make a move. Press Enter to continue..."
    elif status == 'player':
        return "It's your turn to make a move. Enter your command."
    elif status == 'game over':
        if not len(player):
            part = "You won"
        elif not len(computer):
            part = "The computer won"
        elif is_draw():
            part = "it's a draw"
        return f"The game is over. {part}!"


def check_player_command(command):
    error_input = "Invalid input. Please try again."
    error_illegal = "Illegal move. Please try again."

    # Checking if input is in correct format
    if len(command.split()) > 1:
        return False, error_input

    try:
        command_int = int(command)
    except ValueError:
        return False, error_input

    if abs(command_int) not in range(len(player) + 1):
        return False, error_input

    # Checking that not violates the game rules
    if is_legal_move(command_int, player):
        return True, command_int
    else:
        return False, error_illegal


def is_legal_move(command, collection):
    if not command:
        return True
    domino = collection[abs(command) - 1]
    if command < 0:
        return snake[0][0] in domino
    else:
        return snake[-1][1] in domino


def execute_command(command, collection):
    if not command and len(stock):
        collection.append(stock.pop())
    elif command < 0:
        selected = collection.pop(abs(command) - 1)
        if snake[0][0] != selected[1]:
            selected[0], selected[1] = selected[1], selected[0]
        snake.insert(0, selected)
    elif command > 0:
        selected = collection.pop(command - 1)
        if snake[-1][1] != selected[0]:
            selected[0], selected[1] = selected[1], selected[0]
        snake.append(selected)


def generate_computer_command():
    flatten_computer = [item for piece in computer for item in piece]
    flatten_snake = [item for piece in snake for item in piece]
    occurrences = {num: flatten_snake.count(num) + flatten_computer.count(num) for num in flatten_computer}
    scores = {occurrences[domino[0]] + occurrences[domino[1]]: domino for domino in computer}
    scores = dict(sorted(scores.items(), reverse=True))

    for domino in scores.values():
        if snake[0][0] in domino:
            return -(computer.index(domino) + 1)
        elif snake[-1][1] in domino:
            return computer.index(domino) + 1

    return 0


def is_game_over():
    return not len(player) or not len(computer) or is_draw()


def is_draw():
    flatten_snake = [item for piece in snake for item in piece]
    flatten_computer = [item for piece in computer for item in piece]
    flatten_player = [item for piece in player for item in piece]

    if snake[0][0] == snake[len(snake) - 1][1]:
        return flatten_snake.count(snake[0][0]) == 8

    return snake[0][0] not in flatten_computer and snake[0][0] not in flatten_player and snake[-1][1]\
           not in flatten_computer and snake[-1][1] not in flatten_player

    # return False


def change_turn():
    global status
    if status == 'player':
        status = 'computer'
    else:
        status = 'player'


while True:
    #  Creating, shuffling and partitioning the domino
    computer, player, stock = init()

    #  Determining starting piece and first player
    computer_max = calculate_max_double_per_player(computer)
    player_max = calculate_max_double_per_player(player)

    if not computer_max and not player_max:
        continue
    else:
        if computer_max > player_max:
            status = "player"
            snake.append(computer.pop(computer.index(computer_max)))
        else:
            status = "computer"
            snake.append(player.pop(player.index(player_max)))
        break

# Game loop
while True:
    print_interface()

    if status == "player":
        while True:
            result = check_player_command(input())
            if result[0]:
                execute_command(result[1], player)
                break
            else:
                print(result[1])
    elif status == 'computer':
        input()
        execute_command(generate_computer_command(), computer)

    if is_game_over():
        status = 'game over'
        print_interface()
        break
    else:
        change_turn()
