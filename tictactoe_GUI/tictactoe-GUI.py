import tkinter
import tkinter.messagebox
import sqlite3
import sys


class DataAccessLayer:  # class which handles database operation

    def __init__(self):
        """
        constructor for class
        :return: None
        """
        self.conn = sqlite3.connect("tic_tac_toe.db")
        self.cur = self.conn.cursor()

    def get_player_score(self, player_id):
        """
        logs message in file
        :param player_id: player id to to get data
        :return: none
        """
        p = None
        try:
            self.cur.execute("SELECT * from Player where PlayerId={}".format(player_id))
            records = self.cur.fetchall()
            record = records[0]
            player_id = record[0]
            name = record[1]
            mark = record[2]
            l = list([record[3], record[4], record[5]])
            p = Player(name, player_id, mark, l)
        except (sqlite3.OperationalError):
            self.cur.execute(
                "Create table Player (PlayerId INT,PlayerName NVARCHAR(50),PlayingMark CHAR(1),Won INT,Drawn INT,Lost INT)")
            self.conn.commit()
            p = Player("Player{}".format(player_id),player_id, "X" if player_id == 1 else "O", [0, 0, 0])
            self.save_player_data(p)
        except IndexError:
            p = Player("Player{}".format(player_id),player_id, "X" if player_id == 1 else "O", [0, 0, 0])
            self.save_player_data(p)
        return p

    def save_player_data(self, player):
        """
        save player data into database
        :param player: player's object to store in database
        :return:
        """
        self.cur.execute("SELECT * from Player where PlayerId={}".format(player.Id))
        records = self.cur.fetchall()
        player_id = player.Id
        name = player.Name
        mark = player.PlayingMark
        won = player.Statistics["won"]
        draw = player.Statistics["drawn"]
        lost = player.Statistics["lost"]
        if len(records) == 0:
            self.cur.execute(
                "insert into Player values({},'{}','{}',{},{},{})".format(player_id, name, mark, won, draw, lost))
            self.conn.commit()
        else:
            self.cur.execute(
                    "update Player SET PlayerName='{}',PlayingMark='{}',Won={},Drawn={},Lost={} where PlayerId={}".format(
                            name, mark, won, draw, lost, player_id))
            self.conn.commit()

    def __del__(self):
        """
        destructor to close the connections
        :return:
        """
        self.cur.close()
        self.conn.close()


class Player:
    """
    class for player in the game
    """
    def __init__(self, name, player_id, mark, st):
        """
        constructor for player
        :param name: name of player
        :param mark: playing mark X/O
        :return: None
        """
        self.Name = name
        self.Id = player_id
        self.PlayingMark = mark
        self.Statistics = {'won': st[0], 'drawn': st[1], 'lost': st[2]}

    def get_score(self):
        """
        give you the score of player
        :return: int score of player
        """
        return (self.Statistics['won'] * 2) + self.Statistics['drawn'] - self.Statistics['lost']

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

class TicTacToe:
    """
    Main class with logic
    """
    def __init__(self):
        """
        constructor intialize players and fileHandling
        :return:
        """
        self.turn = True
        self.DeckList = []
        self.data_log = DataAccessLayer()
        self.Player1 = self.data_log.get_player_score(1)
        self.Player2 = self.data_log.get_player_score(2)
        self.game_c = self.Player1.Statistics["won"] + self.Player1.Statistics['drawn'] + self.Player1.Statistics[
            'lost']

        self.window = tkinter.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.title("Tic Tac Toe")
        self.height = 370;
        self.width = 300;
        self.window.geometry("{}x{}".format(self.width, self.height))


        p1color = "blue"
        p2color = "blue"
        gccolor = "blue"


        self.lblmsg = "Game has not started"

        self.root = tkinter.Frame(self.window, bg="white")
        self.root.pack(expand=True, fill="both")

        self.nameframe = tkinter.Frame(self.root, bg="white")
        self.p1namelbl = tkinter.Label(self.nameframe, text=self.Player1.Name, bg="white", fg=p1color)
        self.gamenolbl = tkinter.Label(self.nameframe, text="Game No", bg="white", fg=gccolor)
        self.p2namelbl = tkinter.Label(self.nameframe, text=self.Player2.Name, bg="white", fg=p2color)

        self.p1namelbl.pack(side="left", expand=True)
        self.gamenolbl.pack(side="left", expand=True)
        self.p2namelbl.pack(side="left", expand=True)
        self.nameframe.pack(side="top", fill="both")

        self.scoreframe = tkinter.Frame(self.root, bg="white")
        self.lbl_player1_score = tkinter.Label(self.scoreframe, text=self.Player1.get_score(), bg="white", fg=p1color)
        self.lbl_game_counter = tkinter.Label(self.scoreframe, text=self.game_c, bg="white", fg=gccolor)
        self.lbl_player2_score = tkinter.Label(self.scoreframe, text=self.Player2.get_score(), bg="white", fg=p2color)

        self.lbl_player1_score.pack(side="left", expand=True)
        self.lbl_game_counter.pack(side="left", expand=True)
        self.lbl_player2_score.pack(side="left", expand=True)
        self.scoreframe.pack(side="top", fill="both")

        self.canvas = tkinter.Canvas(self.root, width=300, height=300)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.canvasclick)

        self.lbl_messages = tkinter.Label(self.root, text=self.lblmsg, bg="white", fg=gccolor)
        self.lbl_messages.pack(expand=True)

    def on_closing(self):
        """
        handles window closing event
        :return:
        """
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.data_log.save_player_data(self.Player1)
            self.data_log.save_player_data(self.Player2)
            self.window.destroy()

    def canvasclick(self, event):
        """
        handles canvas click event and painting x or o on the canvas
        :param event: click event object
        :return:
        """
        row = event.x // 100
        column = event.y // 100
        game_over, new_game = False, False
        d = self.DeckList[len(self.DeckList) - 1]
        self.lbl_messages["text"] = "canvas clicked at {},{}".format(row, column)
        c = column * 3 + row
        if d.Board[c] == " ":
            if self.turn:
                d.Board[c] = self.Player1.PlayingMark
                self.canvas.create_line(row * 100 + 25, column * 100 + 25, row * 100 + 75, column * 100 + 75, width=4,
                                        fill="black")
                self.canvas.create_line(row * 100 + 25, column * 100 + 75, row * 100 + 75, column * 100 + 25, width=4,
                                        fill="black")
                self.turn = False
                self.lbl_messages["text"] = "Player {} selected cell {}".format(self.Player1.PlayingMark, c)
                game_over, new_game = self.is_game_over(self.Player1, self.Player2)
            else:
                d.Board[c] = self.Player2.PlayingMark
                self.canvas.create_oval(row * 100 + 25, column * 100 + 25, row * 100 + 75, column * 100 + 75, width=4,
                                        outline="black")
                self.turn = True
                self.lbl_messages["text"] = "Player {} selected cell {}".format(self.Player2.PlayingMark, c)
                game_over, new_game = self.is_game_over(self.Player2, self.Player1)
            if game_over:
                if new_game:
                    self.start_game()
                else:
                    self.data_log.save_player_data(self.Player1)
                    self.data_log.save_player_data(self.Player2)
                    self.window.destroy()
        else:
            self.lbl_messages["text"] = "The cell at index {} is already taken!".format(c)

    def is_game_over(self, playerc, playero):
        """
        check for win/lose or draw condition
        :param playerc: current player
        :param playero: other player
        :return:
        """
        game_over = False
        result = False
        c_board = self.DeckList[len(self.DeckList) - 1].Board
        for i in range(3):
            if c_board[i * 3] == c_board[i * 3 + 1] and c_board[i * 3 + 1] == c_board[i * 3 + 2] and c_board[
                        i * 3] != ' ':
                self.canvas.create_line(50, i * 100 + 50, 250, i * 100 + 50, width=2, fill="red")
                game_over = True
            elif c_board[i] == c_board[i + 3] and c_board[i + 3] == c_board[i + 6] and c_board[i] != ' ':
                self.canvas.create_line(i * 100 + 50, 50, i * 100 + 50, 250, width=2, fill="red")
                game_over = True

        if c_board[0] == c_board[4] == c_board[8] and c_board[0] != ' ':
            self.canvas.create_line(50, 50, 250, 250, width=2, fill="red")
            game_over = True
        elif c_board[2] == c_board[4] == c_board[6] and c_board[2] != ' ':
            self.canvas.create_line(50, 250, 250, 50, width=2, fill="red")
            game_over = True

        if game_over:
            playerc.Statistics["won"] += 1
            playero.Statistics["lost"] += 1
            result = tkinter.messagebox.askyesno("Game Over", "{} won!,start new Game?".format(playerc.Name))
        elif c_board.count(' ') == 0:
            playerc.Statistics["drawn"] += 1
            playero.Statistics["drawn"] += 1
            result = tkinter.messagebox.askyesno("Game Over", "Game draw!,start new Game?")
            game_over = True
        return (game_over, result)

    def start_game(self):
        """
        start the game add the deck and keep calling other meathods
        :return: none
        """
        self.DeckList.append(Deck())
        self.turn = True

        self.game_c += 1

        if self.Player1 < self.Player2:
            self.lbl_player1_score.config(fg="blue")
            self.p1namelbl.config(fg="blue")
            self.lbl_player2_score.config(fg="green")
            self.p2namelbl.config(fg="green")
        elif self.Player1 > self.Player2:
            self.lbl_player1_score.config(fg="green")
            self.p1namelbl.config(fg="green")
            self.lbl_player2_score.config(fg="blue")
            self.p2namelbl.config(fg="blue")
        else:
            self.lbl_player1_score.config(fg="blue")
            self.p1namelbl.config(fg="blue")
            self.lbl_player2_score.config(fg="blue")
            self.p2namelbl.config(fg="blue")

        self.window.update()
        self.lbl_game_counter["text"] = self.game_c
        self.lbl_player1_score["text"] = self.Player1.get_score()
        self.lbl_player2_score["text"] = self.Player2.get_score()
        self.lbl_messages["text"] = "New Game Started"
        self.canvas.delete("all")
        self.canvas.create_line(100, 0, 100, 300, width=4, fill="blue")
        self.canvas.create_line(200, 0, 200, 300, width=4, fill="blue")
        self.canvas.create_line(0, 100, 300, 100, width=4, fill="blue")
        self.canvas.create_line(0, 200, 300, 200, width=4, fill="blue")

        self.window.mainloop()


t = TicTacToe()
t.start_game()
