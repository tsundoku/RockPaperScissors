#


from enum import Enum
from random import randint


# 


class Handsign(Enum):

    Rock = 1
    Paper = 2
    Scissors = 3


class Rule:

    def __init__(self, winner, loser, phrase):
        self.winner = winner
        self.loser = loser
        self.phrase = phrase

    def __repr__(self):
        return "{winner} {phrase} {loser}".format(
            winner=self.winner.name,
            phrase=self.phrase,
            loser=self.loser.name)


class Rules:

    def __init__(self):
        self.rules = self.Load()

    def Load(self):
        rules = []
        rules.append(Rule(Handsign.Rock, Handsign.Scissors, "crushes"))        
        rules.append(Rule(Handsign.Paper, Handsign.Rock, "covers"))
        rules.append(Rule(Handsign.Scissors, Handsign.Paper, "cuts"))    
        return rules

    def GetWinningHandsign(self, player_one_handsign, player_two_handsign):
        if player_one_handsign == player_two_handsign:
            return None
        if player_two_handsign in self.GetHandsignsThatWinAgainst(player_one_handsign):
            return player_two_handsign
        if player_two_handsign in self.GetHandsignsThatLoseAgainst(player_one_handsign):
            return player_one_handsign

    def GetRule(self, player_one_handsign, player_two_handsign):
        for rule in self.rules:
            if (rule.winner in [player_one_handsign, player_two_handsign] and
                rule.loser in [player_one_handsign, player_two_handsign]):
                return rule

    def GetHandsignsThatWinAgainst(self, handsign):
        return [rule.winner for rule in self.rules if rule.loser == handsign]

    def GetHandsignsThatLoseAgainst(self, handsign):
        return [rule.loser for rule in self.rules if rule.winner == handsign]        


# 


class PlayerNumber(Enum):

    PlayerOne = 1
    PlayerTwo = 2


class Player:

    def __init__(self, player_number):
        self.player_number = player_number
        self.play_history = []

    def GetLastMove(self):
        if not self.play_history:
            return None
        else:        
            return self.play_history[-1]

    def AppendMove(self, handsign):
        self.play_history.append(handsign)


class HumanPlayer(Player):

    def Play(self, handsign):
        self.AppendMove(handsign)
        return self.GetLastMove()


class ComputerPlayerType(Enum):
    Random = 1
    Tactical = 2


class ComputerPlayer(Player):

    def __init__(self, player_number, computer_player_type, rules):
        Player.__init__(self, player_number)
        self.computer_player_type = computer_player_type
        self.rules = rules

    def Play(self):
        if self.computer_player_type == ComputerPlayerType.Random:
            return self.PlayRandom()
        elif self.computer_player_type == ComputerPlayerType.Tactical:
            return self.PlayTactical()

    def PlayRandom(self):
        handsign = randint(1, len(Handsign))
        self.AppendMove(Handsign(handsign))
        return self.GetLastMove()

    def PlayTactical(self):
        if self.GetLastMove() is None:
            handsign = randint(1, len(Handsign))
            self.AppendMove(Handsign(handsign))
            return self.GetLastMove()
        else:
            tactical_handsign_choices = self.rules.GetHandsignsThatWinAgainst(self.GetLastMove())
            handsign = randint(0, len(tactical_handsign_choices)-1)
            self.AppendMove(tactical_handsign_choices[handsign])
            return self.GetLastMove()


#


class PreMatchView:

    def Headline(self):
        print("\n")
        print("**********************************")
        print("Welcome to Rock - Paper - Scissors")
        print("**********************************")
  
class PreMatchController:

    def __init__(self):
        self.view = PreMatchView()

    def PrintHeadline(self):
        self.view.Headline()


# 


class MatchChoiceModel:

    def __init__(self, rules):
        self.rules = rules
        self.player_one = None
        self.player_two = None


class MatchChoiceView:

    def GetInput(self):
        print("\nPlease choose an option:\n")
        print("(1) to play against an opponent that uses a random play style")
        print("(2) to play against an opponent that uses a tactical play style")
        return input("? ")

    def PrintRangeErrorMessage(self, max_range):
        print("\nYou didn't type a number in the range of 1 to {max_range}\n".format(
            max_range=max_range))


class MatchChoiceController:

    def __init__(self, rules):
        self.model = MatchChoiceModel(rules)
        self.view = MatchChoiceView()

    def GetMatchChoice(self):
        game_raw_input = self.view.GetInput()
        try:
           game_input = int(game_raw_input)
        except:
            self.view.PrintRangeErrorMessage(len(ComputerPlayerType))
            return False
        if game_input not in [x.value for x in ComputerPlayerType]:
            self.view.PrintRangeErrorMessage(len(ComputerPlayerType))
            return False
        elif game_input == ComputerPlayerType.Random.value:
            self.model.player_one = HumanPlayer(PlayerNumber.PlayerOne)
            self.model.player_two = ComputerPlayer(PlayerNumber.PlayerTwo, ComputerPlayerType.Random, self.model.rules)
            return True
        elif game_input == ComputerPlayerType.Tactical.value:
            self.model.player_one = HumanPlayer(PlayerNumber.PlayerOne)
            self.model.player_two = ComputerPlayer(PlayerNumber.PlayerTwo, ComputerPlayerType.Tactical, self.model.rules)
            return True
        else:
            return False


#


class MatchPlayModel:

    def __init__(self, rules, match_rounds):
        self.rules = rules
        self.match_rounds = match_rounds
        self.games = []


class MatchPlayView:

    def Headline(self, match_round, match_rounds):
        print()
        print("*************")
        print("Round: {match_round} of {match_rounds}".format(
            match_round=match_round,
            match_rounds=match_rounds))
        print("*************")
        print()

    def MatchResults(self, match_winner):
        print()
        print("**************")
        print("Match results:")
        print("**************")
        print()
        if match_winner == PlayerNumber.PlayerOne:
            print("Winning Player: Player One\nYou Win\n")
        elif match_winner == PlayerNumber.PlayerTwo:
            print("Winning Player: Player Two\nComputer Wins\n")


class MatchPlayController:

    def __init__(self, rules, match_rounds):
        self.model = MatchPlayModel(rules, match_rounds)
        self.view = MatchPlayView()

    def MatchPlay(self, player_one, player_two):
        match_round = 1
        while (match_round <= self.model.match_rounds):
            self.view.Headline(match_round, self.model.match_rounds)
            game_play_controller = GamePlayController(self.model.rules)
            game_play = False
            while game_play == False:
                game_play = game_play_controller.GamePlay(player_one, player_two)
            else:
                if game_play_controller.model.winning_handsign == None:
                    game_play_controller.GameTie(match_round)
                    continue
                else:
                    self.model.games.append(game_play_controller.model)
                    game_play_controller.GameWinner()
                    match_round = match_round + 1
        self.MatchDecide()
        self.view.MatchResults(self.model.match_winner)

    def MatchDecide(self):
        player_one = 0
        player_two = 0
        for game in self.model.games:
            if game.winning_player == PlayerNumber.PlayerOne:
                player_one = player_one + 1
            elif game.winning_player == PlayerNumber.PlayerTwo:
                player_two = player_two + 1
        if player_one > player_two:
            self.model.match_winner = PlayerNumber.PlayerOne
        elif player_one < player_two:
            self.model.match_winner = PlayerNumber.PlayerTwo
        else:
            self.model.match_winner = None


#


class GamePlayModel:

    def __init__(self, rules):
        self.rules = rules
        self.player_one_handsign = None
        self.player_two_handsign = None
        self.winning_handsign = None
        self.winning_player = None


class GamePlayView:

    def GetInput(self, options):
        print("Please choose an option:")
        for key, value in options.items():
            print("({enumeration}) to use {handsign}".format(
                enumeration=key, handsign=value))
        return input("? ")

    def PrintRangeErrorMessage(self, max_range):
        print("\nYou didn't type a number in the range of 1 to {max_range}\n".format(
            max_range=max_range))

    def GameWinner(self, player_one_handsign, player_two_handsign, winning_handsign, winning_rule, winning_player):
        print()
        print("*************")
        print("Game Results:")
        print("*************")
        print()
        print("Player One: {player_one_handsign}".format(
            player_one_handsign=player_one_handsign.name))
        print("Player Two: {player_two_handsign}".format(
            player_two_handsign=player_two_handsign.name))
        print("Winning Move: {winning_handsign}".format(
            winning_handsign=winning_handsign.name))
        print("Winning Rule: {winning_rule}".format(
            winning_rule=winning_rule))
        print("Winning Player: {winning_player}".format(
            winning_player=winning_player))
        print()

    def GameTie(self, player_one_handsign, player_two_handsign, match_round):
        print()
        print("********************")
        print("Tie, Replay Round {match_round}:".format(
            match_round=match_round))
        print("********************")
        print()
        print("Player One: {player_one_handsign}".format(
            player_one_handsign=player_one_handsign.name))
        print("Player Two: {player_two_handsign}".format(
            player_two_handsign=player_two_handsign.name))
        print()


class GamePlayController:

    def __init__(self, rules):
        self.model = GamePlayModel(rules)
        self.view = GamePlayView()

    def GamePlay(self, player_one, player_two):
        player_one_raw_input = self.view.GetInput({handsign.value: handsign.name for handsign in Handsign})
        try:
            player_one_input = int(player_one_raw_input)
            if player_one_input not in [x.value for x in Handsign]:
                self.view.PrintRangeErrorMessage(len(Handsign))
                return False
            elif player_one_input in [x.value for x in Handsign]:
                self.model.player_one_handsign = player_one.Play(Handsign(player_one_input))
                self.model.player_two_handsign = player_two.Play()
                self.GameDecide(self.model.player_one_handsign, self.model.player_two_handsign)
                return True
            else:
                return False
        except:
            self.view.PrintRangeErrorMessage(len(Handsign))
            return False

    def GameDecide(self, player_one_handsign, player_two_handsign):
        self.model.winning_handsign = self.model.rules.GetWinningHandsign(player_one_handsign, player_two_handsign)
        if self.model.winning_handsign == self.model.player_one_handsign:
            self.model.winning_player = PlayerNumber.PlayerOne
        elif self.model.winning_handsign == self.model.player_two_handsign:
            self.model.winning_player = PlayerNumber.PlayerTwo

    def GameWinner(self):
        self.view.GameWinner(
            self.model.player_one_handsign, 
            self.model.player_two_handsign,
            self.model.winning_handsign,
            self.model.rules.GetRule(self.model.player_one_handsign, self.model.player_two_handsign),
            self.model.winning_player)

    def GameTie(self, match_round):
        self.view.GameTie(
            self.model.player_one_handsign,
            self.model.player_two_handsign,
            match_round)


#


class Interface:

    def __init__(self, match_rounds):
        self.match_rounds = match_rounds
        self.rules = Rules()

    def PlayLoop(self):
        pre_match_controller = PreMatchController()
        match_choice_controller = MatchChoiceController(self.rules)
        match_play_controller = MatchPlayController(self.rules, match_rounds)

        pre_match_controller.PrintHeadline()
        match_choice = False
        while match_choice == False:
            match_choice = match_choice_controller.GetMatchChoice()
        else:
            match_play_controller.MatchPlay(
                match_choice_controller.model.player_one,
                match_choice_controller.model.player_two)


# 


if __name__ == '__main__':
    match_rounds = 3
    interface = Interface(match_rounds)
    interface.PlayLoop()

