from hackathon_bot import *


class Pole:
    def __init__(self, x, y):
        self.y = int(y)
        self.x = int(x)
        self.wsp = 0
        self.is_wall = False


class MyBot(HackathonBot):

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        if not self.initialized_walls:
            self.initialized_walls = True

            #self.pola = [[0 for _ in range(22)] for _ in range(22)]
            for poziom in range(len(self.pola)):
                for pole in range(len(self.pola[poziom])):
                    contains_instance = any(isinstance(item, Wall) for item in game_state.map.tiles[poziom][pole].entities)
                    self.pola[poziom][pole].is_wall = contains_instance
                    #print(poziom, pole)
            #self.przelicz_wszystkie_wspolczyniki_pol(game_state, game_state.my_agent)
            #print(len(game_state.map.tiles))
        self.przelicz_wszystkie_wspolczyniki_pol(game_state)

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass

    def przelicz_wszystkie_wspolczyniki_pol(self, game_state):
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if game_state.map.tiles[poziom][pole].is_visible:
                    self.pola[poziom][pole].wsp = 1
                else:
                    self.pola[poziom][pole].wsp *= 0.8

        ## zmiana współczynnika za każdy widziany element
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if game_state.map.tiles[poziom][pole].is_visible:
                    ## wyjęcie wszystkich elementów z danego pola
                    for entity in game_state.map.tiles[poziom][pole].entities:
                        ## jeśli to wróg odejmujemy i patrzymy czy ma wieżę w naszą stornę
                        if isinstance(entity, PlayerTank):
                            if entity.owner_id != game_state.my_agent.id:
                                self.pola[poziom][pole].wsp -= 5
                                ## jeśli go góry
                                if entity.turret.direction == Direction.UP:
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom_2 < poziom:
                                            self.pola[poziom_2][pole].wsp -= 10
                                ## jeśli w dół
                                if entity.turret.direction == Direction.DOWN:
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom_2 > poziom:
                                            self.pola[poziom_2][pole].wsp -= 10
                                ## jeśli w lewo
                                if entity.turret.direction == Direction.LEFT:
                                    for pole_2 in range(len(self.pola)):
                                        if pole_2 < poziom:
                                            self.pola[pole_2][pole].wsp -= 10
                                ## jeśli w prawo
                                if entity.turret.direction == Direction.LEFT:
                                    for pole_2 in range(len(self.pola)):
                                        if pole_2 > poziom:
                                            self.pola[pole_2][pole].wsp -= 10
        for poziom in self.pola:
            for pole in poziom:
                pole.wsp = 0
        print("-------------------------------------")
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                #print(poziom, pole )
                if self.pola[poziom][pole].is_wall:
                    print("#", end='')
                else:
                    print(' ', end='')


    def __init__(self):
        self.initialized_walls = False
        self.pola = [[0 for _ in range(24)] for _ in range(24)]
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                self.pola[poziom][pole] = Pole(pole, poziom)
                self.pola[poziom][pole].wsp = 0;


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
