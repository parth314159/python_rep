import os


class FileHandling:  # class which handles file operation

    def __init__(self, filename="TicTacToe.txt"):
        """
        constructor for class
        :param filename: File's absolute path where you want to store the output
        :return: None
        """
        self.filename = filename
        self.fw = open(filename, "w")
        self.fw.close()

    def log_msg(self, msg):
        """
        logs message in file
        :param msg: string to log in file
        :return: none
        """
        # self.fw.write("Tic-Tac-Toe tournament between " + p1name + "(X) and " + p2name + "(O):\n")
        with open(self.filename, "a") as self.fw:
            self.fw.write(msg + "\n")


class Player:
    """
    class for player in the game
    """
    def __init__(self, name, mark):
        """
        constructor for player
        :param name: name of player
        :param mark: playing mark X/O
        :return: None
        """
        self.Name = name
        self.PlayingMark = mark
        self.Statistics = {'won': 0, 'drawn': 0, 'lost': 0}

    def get_score(self):
        """
        give you the score of player
        :return: int score of player
        """
        return (self.Statistics['won'] * 2) + self.Statistics['drawn'] - self.Statistics['lost']

    def __str__(self):
        """
        overloaded method
        :return: None
        """
        return "Player:{}, Mark:{}, Score:{}".format(self.Name, self.PlayingMark, self.get_score())

    def __lt__(self, other):
        """
        overloaded < operator not being used right now
        :param other: other
        :return:
        """
        return self.get_score() < other.get_score()


class Deck:
    """
    Deck class to represent the deck
    """
    def __init__(self):
        """
        constructor for Deck
        :return:
        """
        self.Board = [' ' for x in range(9)]
        # self.Player1Choices = []
        # self.Player2Choices = []

    def __str__(self):
        board_str = ''
        for i in range(3):
            board_str += "     |     |     \n  " + self.Board[i * 3] + "  |  " \
                         + self.Board[i * 3 + 1] + "  |  " + self.Board[i * 3 + 2] + " \n"
            if i < 2:
                board_str += "_____|_____|_____\n"
            else:
                board_str += "     |     |     \n"
        return board_str


class TicTacToe:
    """
    Main class with logic
    """
    def __init__(self):
        """
        constructor intialize players and fileHandling
        :return:
        """
        self.DeckList = []
        p1name = input("Enter player X Name:")
        self.Player1 = Player(p1name, "X")
        p2name = input("Enter player O Name:")
        self.Player2 = Player(p2name, "O")
        self.File_log = FileHandling()
        self.File_log.log_msg("Tic-Tac-Toe tournament between " + p1name + "(X) and " + p2name + "(O):-")

    def validate_user_input(self, player):
        """
        validate user's input
        :param player: player's object who is currently playing
        :return:
        """
        while True:
            try:
                d = self.DeckList[len(self.DeckList) - 1]
                user_inp = int(input("Enter Player " + player.PlayingMark + " move:"))
                if user_inp < 0 or user_inp > 8:
                    print("invalid move, move should be between 0 and 8")
                elif d.Board[user_inp] != ' ':
                    print("The cell at index {} was already taken!".format(user_inp))
                else:
                    return user_inp
            except ValueError:
                print("invalid move, move should be an integer")

    def is_game_over(self, playerc, playero):
        """
        check for win/lose or draw condition
        :param playerc: current player
        :param playero: other player
        :return:
        """
        game_over = False
        c_board = self.DeckList[len(self.DeckList) - 1].Board

        for i in range(3):
            if c_board[i * 3] == c_board[i * 3 + 1] and c_board[i * 3 + 1] == c_board[i * 3 + 2] and c_board[
                        i * 3] != ' ':
                game_over = True
            elif c_board[i] == c_board[i + 3] and c_board[i + 3] == c_board[i + 6] and c_board[i] != ' ':
                game_over = True

        if c_board[0] == c_board[4] == c_board[8] and c_board[0] != ' ':
            game_over = True
        elif c_board[2] == c_board[4] == c_board[6] and c_board[2] != ' ':
            game_over = True

        if game_over:
            print("Player {} won".format(playerc.PlayingMark))
            playerc.Statistics["won"] += 1
            playero.Statistics["lost"] += 1
        elif c_board.count(' ') == 0:
            print("Draw No more Moves!")
            playerc.Statistics["drawn"] += 1
            playero.Statistics["drawn"] += 1
            game_over = True

        if game_over:
            d = self.DeckList[len(self.DeckList) - 1]
            self.File_log.log_msg("Game Number {} :".format(len(self.DeckList)) + "\n" + d.__str__())

        return game_over

    def get_user_input(self, playerc, playero):
        """
        get input from the user and validate by calling meathod
        :param playerc: object of current player
        :param playero: object of the other player
        :return:
        """
        usr_inp = self.validate_user_input(playerc)
        d = self.DeckList[len(self.DeckList) - 1]
        d.Board[usr_inp] = playerc.PlayingMark
        print(self.DeckList[len(self.DeckList) - 1])
        check_game = self.is_game_over(playerc, playero)
        return check_game

    def start_game(self):
        """
        start the game add the deck and keep calling other meathods
        :return: none
        """
        self.DeckList.append(Deck())
        turn = True
        game_over = False
        while not game_over:
            if turn:
                game_over = self.get_user_input(self.Player1, self.Player2)
            else:
                game_over = self.get_user_input(self.Player2, self.Player1)
            turn = not turn
            if game_over:
                print("Game Over!")
                print(self.Player1)
                print(self.Player2)
        while True:
            #os.system('cls')
            new_game = input("do you want to play again (Y/N) :")
            if new_game.lower() == "y":
                self.start_game()
                return
            elif new_game.lower() == "n":
                self.File_log.log_msg("Final Score:\n" + self.Player1.__str__() + "\n" + self.Player2.__str__())
                return
            else:
                print("Invalid Input, Please enter Y/N")


t = TicTacToe()
t.start_game()
