import heapq
import math

from hackathon_bot import *


class Pole:
    def __init__(self, x, y):
        self.y = int(y)
        self.x = int(x)
        self.wsp = 0
        self.is_wall = False


class MyBot(HackathonBot):

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def a_star(self, walls, start, goal):
        rows, cols = len(walls), len(walls[0])
        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            neighbors = [
                (current[0] + 1, current[1]),
                (current[0] - 1, current[1]),
                (current[0], current[1] + 1),
                (current[0], current[1] - 1)
            ]

            for neighbor in neighbors:
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and walls[neighbor[0]][neighbor[1]] == 0:
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None


    def get_directions(self, walls, start, goal):

        directions = list()
        tiles = self.a_star(walls, start, goal)
        if tiles is None:
            return None
        previous = tiles[0]
        directions.append('u')
        for tile in tiles[1:]:
            dir = (tile[0] - previous[0], tile[1] - previous[1])
            previous = tile
            print("essa", directions[-1:])
            if dir[1] == 1:
                if directions[-1] == 'u':
                    directions.append('e')
                if directions[-1] == 'd':
                    directions.append('q')
                directions.append('r')
            if dir[1] == -1:
                if directions[-1] == 'u':
                    directions.append('q')
                if directions[-1] == 'd':
                    directions.append('e')
                directions.append('l')
            if dir[0] == -1:
                if directions[-1] == 'l':
                    directions.append('e')
                if directions[-1] == 'r':
                    directions.append('q')
                directions.append('u')
            if dir[0] == 1:
                if directions[-1] == 'l':
                    directions.append('q')
                if directions[-1] == 'r':
                    directions.append('e')
                directions.append('d')
        return directions


    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        if not self.initialized_walls:
            #self.initialized_walls = True
            #self.enemies = list()
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
        walkable = [[0 for _ in range(24)] for _ in range(24)]
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                contains_instance = any(isinstance(item, (Wall, Bullet, DoubleBullet, Laser, Mine, PlayerTank)) for item in game_state.map.tiles[poziom][pole].entities)
                if contains_instance:
                    walkable[poziom][pole] = 1

        self.enemies = list()
        wsp_wygasania_niewidocznych = 0.8
        wsp_poczatkowy_widocznych = 1
        wsp_pola_z_wrogiem = -5
        wsp_obserwowanego_pola = -10
        wsp_item_laser = 20
        wsp_item_double_bullet = 10
        wsp_item_mine = 5
        wsp_item_radar = 10
        wsp_item_unknown = -20
        wsp_bullet = -20
        wsp_double_bullet = -40
        wsp_laser = -80
        wsp_mine = -40
        wsp_wall = -1000

        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                for entity in game_state.map.tiles[poziom][pole].entities:
                    contains_instance = any(
                        isinstance(item, Wall) for item in game_state.map.tiles[poziom][pole].entities)
                    if contains_instance:
                        walkable[poziom][pole] = 1
                        #self.my_position = (poziom, pole)
                    if isinstance(entity, PlayerTank):
                        if entity.owner_id == game_state.my_agent.id:
                            print('------------------')
                            print((poziom, pole))
                            self.my_position = (poziom, pole)
                        else:
                            self.enemies.append((poziom, pole))
                            walkable[poziom][pole] = 1
                    if isinstance(entity, Laser) or isinstance(entity, Bullet) or isinstance(entity, Mine) or isinstance(entity, DoubleBullet):
                        walkable[poziom][pole] = 1

                if self.pola[poziom][pole].is_wall:
                    walkable[poziom][pole] = 1
                    self.pola[poziom][pole].wsp = wsp_wall
                    continue
                if game_state.map.tiles[poziom][pole].is_visible:
                    self.pola[poziom][pole].wsp = wsp_poczatkowy_widocznych
                else:
                    self.pola[poziom][pole].wsp *= wsp_wygasania_niewidocznych

        #print(self.a_star(walkable, (1, 1), (4, 4)))
        #print(self.get_directions(walkable, (1, 1), (4,4)))
        #for p in self.a_star(walkable, (1,1), (4,4)):
        #    print(self.pola[p[0]][p[1]].is_wall)
        #print(self.my_position[1])
        ## zmiana współczynnika za każdy widziany element
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if self.pola[poziom][pole].is_wall:
                    break
                if game_state.map.tiles[poziom][pole].is_visible:
                    ## wyjęcie wszystkich elementów z danego pola
                    for entity in game_state.map.tiles[poziom][pole].entities:
                        ## jeśli to wróg odejmujemy i patrzymy czy ma wieżę w naszą stornę
                        if isinstance(entity, PlayerTank):
                            print("tank", entity)
                            if entity.owner_id != game_state.my_agent.id:
                                self.pola[poziom][pole].wsp += wsp_pola_z_wrogiem
                                ## jeśli go góry
                                if entity.turret.direction is Direction.UP:
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom_2 < poziom:
                                            self.pola[poziom_2][pole].wsp += wsp_obserwowanego_pola
                                            if self.pola[poziom_2][pole].is_wall:
                                                break
                                ## jeśli w dół
                                elif entity.turret.direction is Direction.DOWN:
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom_2 > poziom:
                                            self.pola[poziom_2][pole].wsp += wsp_obserwowanego_pola
                                            if self.pola[poziom_2][pole].is_wall:
                                                break
                                ## jeśli w lewo
                                elif entity.turret.direction is Direction.LEFT:
                                    for pole_2 in range(len(self.pola)):
                                        if pole_2 < pole:
                                            self.pola[poziom][pole_2].wsp += wsp_obserwowanego_pola
                                            if self.pola[poziom][pole_2].is_wall:
                                                break
                                ## jeśli w prawo
                                elif entity.turret.direction is Direction.RIGHT:
                                    for pole_2 in range(len(self.pola)):
                                        if pole_2 > pole:
                                            self.pola[poziom][pole_2].wsp += wsp_obserwowanego_pola
                                            if self.pola[poziom][pole_2].is_wall:
                                                break
                        ## jeśli jest itemem dodajemy współczynniki
                        elif isinstance(entity, Item):
                            if entity.type is ItemType.LASER:
                                self.pola[poziom][pole].wsp += wsp_item_laser
                            if entity.type is ItemType.DOUBLE_BULLET:
                                self.pola[poziom][pole].wsp += wsp_item_double_bullet
                            if entity.type is ItemType.MINE:
                                self.pola[poziom][pole].wsp += wsp_item_mine
                            if entity.type is ItemType.RADAR:
                                self.pola[poziom][pole].wsp += wsp_item_radar
                            if entity.type is ItemType.UNKNOWN:
                                self.pola[poziom][pole].wsp += wsp_item_unknown
                        elif isinstance(entity, Bullet):
                            self.pola[poziom][pole].wsp += wsp_bullet
                        elif isinstance(entity, DoubleBullet):
                            self.pola[poziom][pole].wsp += wsp_double_bullet
                        elif isinstance(entity, Laser):
                            self.pola[poziom][pole].wsp += wsp_laser
                        elif isinstance(entity, Mine):
                            self.pola[poziom][pole].wsp += wsp_mine

        print("-------------------------------------")
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if self.pola[poziom][pole].is_wall:
                    print("#", end='  ')
                else:
                    print(math.floor(self.pola[poziom][pole].wsp), end='  ')
            print()

    def __init__(self):
        self.enemies = list()
        self.my_position = tuple()
        self.initialized_walls = False
        self.pola = [[0 for _ in range(24)] for _ in range(24)]
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                self.pola[poziom][pole] = Pole(pole, poziom)
                self.pola[poziom][pole].wsp = 0


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
