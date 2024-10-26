import heapq
import math

from hackathon_bot import *
from test import find_closest_point

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
wsp_podnoszenia_przy_pelnym_ekwipunku = 0.6
wsp_stref = 10


class Pole:
    def __init__(self, x, y):
        self.y = int(y)
        self.x = int(x)
        self.wsp = 0
        self.is_wall = False


def find_closest_point(points, player):
    closest_point = None
    min_distance = float('inf')  # Initialize with a very large number

    for point in points:
        distance = math.sqrt((point[0] - player[0]) ** 2 + (point[1] - player[1]) ** 2)

        if distance < min_distance:
            min_distance = distance
            closest_point = point

    return closest_point


def get_rotation(entity, position):
    x, y = entity
    px, py = position

    vertical_distance = y - py
    horizontal_distance = x - px
    if abs(vertical_distance) >= abs(horizontal_distance):
        return "l" if vertical_distance > 0 else "r"
    elif abs(horizontal_distance) > abs(vertical_distance):
        return "u" if horizontal_distance > 0 else "d"


def rotation(letter, pos):
    if letter == 'l':
        if pos == 'u':
            return 'e'
        if pos == 'd':
            return 'q'
        if pos == 'r':
            return 'q'
    if letter == 'r':
        if pos == 'u':
            return 'q'
        if pos == 'd':
            return "e"
        if pos == 'l':
            return 'e'
    if letter == 'u':
        if pos == 'l':
            return 'e'
        if pos == 'r':
            return 'q'
        if pos == 'd':
            return 'q'
    if letter == 'd':
        if pos == 'l':
            return 'q'
        if pos == 'r':
            return 'e'
        if pos == 'u':
            return 'e'


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
        print(self.enemies)
        print(self.my_position)
        if not self.initialized_walls:
            #self.initialized_walls = True
            #self.enemies = list()
            for poziom in range(len(self.pola)):
                for pole in range(len(self.pola[poziom])):
                    contains_instance = any(isinstance(item, Wall) for item in game_state.map.tiles[poziom][pole].entities)
                    self.pola[poziom][pole].is_wall = contains_instance

        najwyzszy_wsp_pol = self.pola[0][0].wsp
        najlepsze_pole = self.pola[0][0]

        self.przelicz_wszystkie_wspolczyniki_pol(game_state)
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if self.pola[poziom][pole].wsp > najwyzszy_wsp:
                    najwyzszy_wsp_pol = self.pola[poziom][pole].wsp
                    najlepsze_pole = self.pola[poziom][pole]

    def ruch_wiezy(self, gamestate):
        return rotation(get_rotation(self.my_position, find_closest_point(self.enemies, self.my_position)), 'u')

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass

    def przelicz_wszystkie_wspolczyniki_pol(self, game_state):
        walkable = [[0 for _ in range(24)] for _ in range(24)]
        self.enemies = list()
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                contains_instance = any(isinstance(item, (Wall, Bullet, DoubleBullet, Laser, Mine, PlayerTank)) for item in game_state.map.tiles[poziom][pole].entities)
                if contains_instance:
                    walkable[poziom][pole] = 1
                contains_instance = any(
                    isinstance(item, (PlayerTank)) for item in
                    game_state.map.tiles[poziom][pole].entities)
                if contains_instance:
                    self.enemies.append((poziom, pole))
                contains_instance = any(
                    isinstance(item, (AgentTank)) for item in
                    game_state.map.tiles[poziom][pole].entities)
                if contains_instance:
                    self.my_position = (poziom, pole)
        while self.my_position in self.enemies:
            self.enemies.remove(self.my_position)

        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if self.pola[poziom][pole].is_wall:
                    self.pola[poziom][pole].wsp = wsp_wall
                    continue
                if game_state.map.tiles[poziom][pole].is_visible:
                    self.pola[poziom][pole].wsp = wsp_poczatkowy_widocznych
                else:
                    self.pola[poziom][pole].wsp *= wsp_wygasania_niewidocznych

        for zone in game_state.map.zones:
            for i in range(zone.height):
                for j in range(zone.width):
                    self.pola[zone.y+i][zone.x+j].wsp += wsp_stref

        #print(self.a_star(walkable, (1, 1), (4, 4)))
        #print(self.get_directions(walkable, (1, 1), (4,4)))
        #for p in self.a_star(walkable, (1,1), (4,4)):
        #    print(self.pola[p[0]][p[1]].is_wall)
        #print(self.my_position[1])

        obecny_wsp_podnoszenia = wsp_podnoszenia_przy_pelnym_ekwipunku
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
                        #jeśli nie mamy itema ustawiamy wsp podnoszenia na 1
                        elif isinstance(entity, AgentTank):
                            if entity.secondary_item is None:
                                obecny_wsp_podnoszenia = 1
                        ## jeśli jest itemem dodajemy wsp mnożony przez współczynnik podnoszenia
                        elif isinstance(entity, Item):
                            if entity.type is ItemType.LASER:
                                self.pola[poziom][pole].wsp += wsp_item_laser*obecny_wsp_podnoszenia
                            if entity.type is ItemType.DOUBLE_BULLET:
                                self.pola[poziom][pole].wsp += wsp_item_double_bullet*obecny_wsp_podnoszenia
                            if entity.type is ItemType.MINE:
                                self.pola[poziom][pole].wsp += wsp_item_mine*obecny_wsp_podnoszenia
                            if entity.type is ItemType.RADAR:
                                self.pola[poziom][pole].wsp += wsp_item_radar*obecny_wsp_podnoszenia
                            if entity.type is ItemType.UNKNOWN:
                                self.pola[poziom][pole].wsp += wsp_item_unknown
                        ## jeśli jest jakimś rodzajem pocisku dodajemy ujemny współczynnik
                        elif isinstance(entity, Bullet):
                            self.pola[poziom][pole].wsp += wsp_bullet
                        elif isinstance(entity, DoubleBullet):
                            self.pola[poziom][pole].wsp += wsp_double_bullet
                        elif isinstance(entity, Laser):
                            self.pola[poziom][pole].wsp += wsp_laser
                        elif isinstance(entity, Mine):
                            self.pola[poziom][pole].wsp += wsp_mine

        # print("-------------------------------------")
        # for poziom in range(len(self.pola)):
        #     for pole in range(len(self.pola[poziom])):
        #         if self.pola[poziom][pole].is_wall:
        #             print("#", end='  ')
        #         else:
        #             print(math.floor(self.pola[poziom][pole].wsp), end='  ')
        #     print()
        #

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
