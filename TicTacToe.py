import random


# Function to print Tic Tac Toe
def print_tic_tac_toe(values):
    print("\n")
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(values[0], values[1], values[2]))
    print('\t_____|_____|_____')

    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(values[3], values[4], values[5]))
    print('\t_____|_____|_____')

    print("\t     |     |")

    print("\t  {}  |  {}  |  {}".format(values[6], values[7], values[8]))
    print("\t     |     |")
    print("\n")


def check_winner(values):
    """Überprüft, ob es einen Gewinner im Tic-Tac-Toe-Spiel gibt."""

    # Gewinnmuster (Indexe des Spielfelds)
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontale
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertikale
        [0, 4, 8], [2, 4, 6]  # Diagonale
    ]

    for combination in winning_combinations:
        a, b, c = combination
        if values[a] == values[b] == values[c] and values[a] in ['X', 'O']:
            return values[a]  # Gibt den Gewinner ('X' oder 'O') zurück

    if all(v in ['X', 'O'] for v in values):
        return "Tie"  # Gibt "Tie" zurück, wenn das Feld voll ist und kein Gewinner gefunden wurde

    return None  # Es gibt keinen Gewinner, das Spiel ist noch nicht vorbei


def get_game_mode():
    """Fragt den Benutzer nach dem Spielmodus (Singleplayer oder Multiplayer) und gibt die Auswahl zurück."""
    while True:
        mode = input("Möchtest du Singleplayer (s) oder Multiplayer (m) spielen? (s/m): ").lower()
        if mode in ['s', 'm']:
            return mode
        else:
            print("Ungültige Eingabe. Bitte 's' für Singleplayer oder 'm' für Multiplayer eingeben.")


def get_player_input(cur_player):
    """Fordert den Spieler auf, eine Zahl zwischen 1 und 9 für eine Box auszuwählen."""
    while True:
        try:
            input_str = input(f"\nSpieler {cur_player} ist an der Reihe. Welches Feld? (1-9): ")
            input_num = int(input_str)

            if 1 <= int(input_str) <= 9:
                if values[input_num - 1] != ' ':
                    print("Feld bereits besetzt. Wähle ein anderes Feld!!")
                else:
                    return input_num
            else:
                print("Ungültige Eingabe. Bitte wähle eine Zahl zwischen 1 und 9.")
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine Zahl ein.")


def computer_move(values):
    """Wählt einen Zug für den Computer (Spieler O) basierend auf einer einfachen Logik."""

    # 1. Versuche zu gewinnen (wenn möglich)
    for i in range(9):
        temp_values = list(values)  # Kopie der Spielfeldliste
        if temp_values[i] not in ['X', 'O']:  # überprüfe, ob das Feld frei ist
            temp_values[i] = 'O'
            if check_winner(temp_values) == 'O':
                return i + 1  # wenn durch diesen Zug der Computer gewinnt, dann wähle das Feld

    # 2. Versuche zu blockieren (wenn Spieler X gewinnen würde)
    for i in range(9):
        temp_values = list(values)  # Kopie der Spielfeldliste
        if temp_values[i] not in ['X', 'O']:  # überprüfe, ob das Feld frei ist
            temp_values[i] = 'X'
            if check_winner(temp_values) == 'X':
                return i + 1  # wenn Spieler X mit diesem Zug gewinnt, dann wähle das Feld um zu blockieren

    # 3. Wähle ein zufälliges, freies Feld
    available_moves = [i + 1 for i, v in enumerate(values) if v not in ['X', 'O']]
    if available_moves:
        return random.choice(available_moves)

    return None  # Alle Felder sind besetzt (sollte nicht passieren)


if __name__ == "__main__":
    game_mode = get_game_mode()
    values = [' ' for x in range(9)]

    if game_mode == 's':
        print("\nDu hast Singleplayer gewählt.")
        print("\nSingleplayer Modus ist noch nicht verfügbar, wähle Multiplayer.")

        cur_player = 'X'

        while True:
            if cur_player == 'X':
                box = get_player_input(cur_player)  # Spieler gibt die Box ein
            else:
                box = computer_move(values)  # Computer berechnet den Zug

            index = box - 1
            values[index] = cur_player

            print_tic_tac_toe(values)
            winner = check_winner(values)

            if winner in ['X']:
                print(f'Gratuliere - Du gewinnst !!!')
                break
            elif winner == 'O':
                print(f'Schade - Der Computer gewinnt !!!')
                break
            elif winner == 'Tie':
                print(f'Unentschieden - Keiner gewinnt.')
                break

            if cur_player == 'O':
                cur_player = 'X'
            elif cur_player == 'X':
                cur_player = 'O'

    elif game_mode == 'm':
        print("\nDu hast Multiplayer gewählt.")

        cur_player = 'X'
        while True:

            box = get_player_input(cur_player)

            # Stores the positions occupied by X and O
            player_pos = {'X': [], 'O': []}

            index = box - 1
            values[index] = cur_player

            print_tic_tac_toe(values)
            winner = check_winner(values)

            if winner in ['X', 'O']:
                print(f'Gratuliere - Spieler {winner} gewinnt !!!')
                break
            elif winner == 'Tie':
                print(f'Unentschieden - Keiner gewinnt.')
                break

            if cur_player == 'O':
                cur_player = 'X'
            elif cur_player == 'X':
                cur_player = 'O'
