from hackathon_bot import *


class Pole:
    def __init__(self, x, y):
        self.y = int(y)
        self.x = int(x)
        self.wsp = 0


class MyBot(HackathonBot):

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        pass
        self.przelicz_wszystkie_wspolczyniki_pol(game_state, game_state.my_agent)

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass


    def przelicz_wszystkie_wspolczyniki_pol(self, game_state, player_state):
        for poziom in self.pola:
            for pole in poziom:
                pole.wsp = 0

        for poziom in self.pola:
            print()
            for pole in poziom:
                print(pole.wsp, end=', ')
        print()


    def __init__(self):
        self.pola = [[0 for _ in range(22)] for _ in range(22)]
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                self.pola[poziom][pole] = Pole(pole, poziom)


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
