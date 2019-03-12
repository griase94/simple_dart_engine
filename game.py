from player import Throw, Player


class Game:
    def __init__(self, players, point_goal, double_out):
        self.players = players
        self.current_player = 0
        self.point_goal = point_goal
        self.double_out = double_out
        self.game_over = False
        # start first round for first player
        self.players[0].new_round()
        print("New {} point game! Double out: {}. {} starts!".format(point_goal, double_out, self.players[0].name))

    def throw(self, player_index, number, multiplier):
        if self.game_over:
            print("Game is already over, {} won!".format(self.get_current_player().name))
        elif self.current_player != player_index:
            print("Not player {}'s turn".format(player_index + 1))
        elif number > 20 and number != 25 or number < 0:
            print("{} x {} is not a valid throw (1)".format(number, multiplier))
        elif number == 25 and (multiplier > 2 or multiplier < 1):
            print("{} x {} is not a valid throw (2)".format(number, multiplier))
        elif multiplier < 1 or multiplier > 3:
            print("{} x {} is not a valid throw (3)".format(number, multiplier))
        else:
            throw = Throw(number, multiplier)
            player = self.get_current_player()
            if throw.get_score() + player.get_score() > self.point_goal:
                player.remove_last_round()
                points_left = self.point_goal - player.get_score()
                print("{} overthrows with a {}x{} He/She has {} points left.".format(player.name, number, multiplier,
                                                                                     points_left))
                self.next_player()
            else:
                third_throw = player.throw(throw)
                points_left = self.point_goal - player.get_score()
                print("{} throws a {}x{}! He/She has {} points left.".format(player.name, number, multiplier,
                                                                             points_left))
                if player.is_done(self.double_out, self.point_goal):
                    print("{} wins!".format(player.name))
                    self.game_over = True
                elif third_throw:
                    self.next_player()

    def get_current_player(self):
        return self.players[self.current_player]

    def next_player(self):
        if self.current_player < len(self.players) - 1:
            self.current_player += 1
        elif self.current_player == len(self.players) - 1:
            self.current_player = 0
        print("{}'s turn now...".format(self.get_current_player().name))
        self.get_current_player().new_round()

    def last_player(self):
        if self.current_player > 0:
            self.current_player -= 1
        else:
            self.current_player = len(self.players) - 1
        print("{}'s turn now...".format(self.get_current_player().name))

    def undo_throw(self):
        switch_player = self.get_current_player().undo_throw()
        if switch_player:
            if self.current_player == 0 and self.get_current_player().is_first_throw():
                print("Can't undo: game has just started")
            else:
                self.get_current_player().remove_last_round()
                self.last_player()
                # recursively call function again so last throw of last player will be removed
                self.undo_throw()
        else:
            player = self.get_current_player()
            points_left = self.point_goal - player.get_score()
            print("Undid {}'s throw. He/She has {} points left.".format(player.name, points_left))
