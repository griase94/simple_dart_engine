class Player:

    def __init__(self, name):
        self.name = name
        self.rounds = []

    def get_score(self):
        score = 0
        for x in self.rounds:
            score += x.get_score()
        return score

    def is_done(self, double_out, points_goal):
        zero = self.get_score() == points_goal
        if double_out:
            return zero and self.rounds[-1].last_is_double()
        else:
            return zero

    def throw(self, throw):
        return self.rounds[-1].add_throw(throw)

    def undo_throw(self):
        # returns true if round was already empty ->other players turn
        return self.rounds[-1].undo_throw() == -1

    def new_round(self):
        self.rounds.append(Round())

    def remove_last_round(self):
        self.rounds.pop()

    def is_first_throw(self):
        return len(self.rounds) == 1 and self.rounds[0].is_empty()


class Round:
    def __init__(self):
        self.throws = []

    def add_throw(self, throw):
        if len(self.throws) < 3:
            self.throws.append(throw)
            # return true when last throw
        return len(self.throws) == 3

    def undo_throw(self):
        if self.throws:  # if empty_list will evaluate as false.
            throw = self.throws.pop()
            print("Undoing {}. throw of round: {}x{}".format(len(self.throws)+1, throw.number, throw.multiplier))
            # return size of list
            return len(self.throws)
        else:
            # return -1 if list was already empty
            return -1

    def get_score(self):
        # sum the scores of all the throws
        score = 0
        for x in self.throws:
            score += x.get_score()
        return score

    def is_done(self):
        return len(self.throws) == 3

    def last_is_double(self):
        return self.throws[-1].multiplier == 2

    def is_empty(self):
        return len(self.throws) == 0


class Throw:
    def __init__(self, number, multiplier):
        self.number = number
        self.multiplier = multiplier

    def get_score(self):
        return self.number * self.multiplier
