import heapq
import math
import random

from hackathon_bot import *

wsp_wygasania_niewidocznych = 0.8
wsp_poczatkowy_widocznych = 0.5
wsp_pola_z_wrogiem = -10
wsp_obserwowanego_pola = -3
wsp_nieobserwowanego_pola = 5
wsp_pod_graczem = -3

wsp_item_laser = 30
wsp_item_double_bullet = 15
wsp_item_mine = 10
wsp_item_radar = 15
wsp_item_unknown = -20

wsp_bullet = -20
wsp_double_bullet = -40
wsp_laser = -80
wsp_mine = -40
wsp_wall = -1000

wsp_podnoszenia_przy_pelnym_ekwipunku = 0.6

wsp_stref_neutral = 5
wsp_stref_being_captured = 5
wsp_stref_captured = 2.5
wsp_stref_being_contested = 2
wsp_stref_being_retaken = 4

wsp_rage = 1.5
wsp_min_score_per_tick_rage = 1

rage_wsp_pola_z_wrogiem = 0.8
rage_wsp_obserwowanego_pola = -30
rage_wsp_item_laser = 40
rage_wsp_item_double_bullet = 20
rage_wsp_item_mine = 10
rage_wsp_item_radar = 15
rage_wsp_item_unknown = -15
rage_wsp_stref = 30


class Pole:
    def __init__(self, x, y):
        self.y = int(y)
        self.x = int(x)
        self.wsp = 0
        self.is_wall = False

import math

def add_vectors(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def interpolate(value, range_start, range_end, target_start, target_end):
    ratio = (value - range_start) / (range_end - range_start)
    return target_start + ratio * (target_end - target_start)

def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def get_direction_of_player(position, game_state: GameState):
    return game_state.map.tiles[position[0]][position[1]].entities[0].direction

def get_turret_direction_of_player(position, game_state: GameState):
    return game_state.map.tiles[position[0]][position[1]].entities[0].turret.direction

def convert_to_directions(letter):
    if letter == 'u':
        return Direction.UP
    if letter == 'd':
        return Direction.DOWN
    if letter == 'l':
        return Direction.LEFT
    if letter == 'r':
        return Direction.RIGHT
    return None

def convert_to_letters(direction: Direction):
    if direction is Direction.UP:
        return 'u'
    if direction is Direction.LEFT:
        return 'l'
    if direction is Direction.RIGHT:
        return 'r'
    if direction is Direction.DOWN:
        return 'd'

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


    def get_directions(self, walls, start, goal, direction):

        directions = list()
        tiles = self.a_star(walls, start, goal)
        if tiles is None:
            return None
        previous = tiles[0]
        directions.append(direction)
        for tile in tiles[1:]:
            dir = (tile[0] - previous[0], tile[1] - previous[1])
            previous = tile
            #print("essa", directions[-1:])
            if dir[1] == 1:
                if directions[-1] == 'u':
                    directions.append('e')
                if directions[-1] == 'd':
                    directions.append('q')
                if directions[-1] == 'l':
                    directions.append('q')
                directions.append('r')
            if dir[1] == -1:
                if directions[-1] == 'u':
                    directions.append('q')
                if directions[-1] == 'd':
                    directions.append('e')
                if directions[-1] == 'r':
                    directions.append('e')
                directions.append('l')
            if dir[0] == -1:
                if directions[-1] == 'l':
                    directions.append('e')
                if directions[-1] == 'r':
                    directions.append('q')
                if directions[-1] == 'd':
                    directions.append('q')
                directions.append('u')
            if dir[0] == 1:
                if directions[-1] == 'l':
                    directions.append('q')
                if directions[-1] == 'r':
                    directions.append('e')
                if directions[-1] == 'u':
                    directions.append('e')
                directions.append('d')
        return directions


    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        if game_state.my_agent.is_dead:
            Pass()
        self.my_tick += 1

        if game_state.my_agent.is_dead:
            return Pass()

        if not self.initialized_walls:
            self.initialized_walls = True
            #self.enemies = list()
            for poziom in range(len(self.pola)):
                for pole in range(len(self.pola[poziom])):
                    contains_instance = any(isinstance(item, Wall) for item in game_state.map.tiles[poziom][pole].entities)
                    self.pola[poziom][pole].is_wall = contains_instance

        najwyzszy_wsp_pol = self.pola[0][0].wsp
        najlepsze_pole = self.pola[0][0]


        #if self.my_tick % 30 == 0:
        #    self.show_map()

        self.przelicz_wszystkie_wspolczyniki_pol(game_state)
        if get_direction_of_player(self.my_position, game_state) is not get_turret_direction_of_player(self.my_position, game_state):
            return Rotation(None, RotationDirection.RIGHT)
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if self.pola[poziom][pole].wsp * interpolate(distance(self.my_position, (poziom, pole)), 0, 30, 1, 0.7) > najwyzszy_wsp_pol:
                    najwyzszy_wsp_pol = self.pola[poziom][pole].wsp
                    najlepsze_pole = self.pola[poziom][pole]
        najwyzszy_wsp_pol *= interpolate(distance(self.my_position, (poziom, pole)), 0, 30, 1, 0.7)
        #t = self.get_directions(self.walkable, (0, 2), (2, 8), 'u')

        if self.counter == 30:
            self.counter = 0

        if self.counter == 0:
            self.xv, self.yv = random.randint(1, 21), random.randint(1, 21)
            tils = list()
            zone = game_state.map.zones[0]
            for i in range(zone.height):
                for j in range(zone.width):
                    tils.append((zone.y + i, zone.x + j))
            r = random.randint(1, 4)
            if False:
                if not self.pola[self.xv][self.yv].is_wall:
                    self.counter += 1
            else:
                self.xv, self.yv = random.choice(tils)
                #print((self.xv, self.yv))
        else:
            self.counter += 1
        self.pola[self.xv][self.yv].wsp += 3
        #print()
        if self.counter < 30:
            #print('a')
            dirs = self.get_directions(self.walkable, (self.my_position[0], self.my_position[1]), (self.xv, self.yv), convert_to_letters(get_direction_of_player(self.my_position, game_state)))
        else:
            #print('b')
            dirs = self.get_directions(self.walkable, (self.my_position[0], self.my_position[1]), (najlepsze_pole.x, najlepsze_pole.y), convert_to_letters(get_direction_of_player(self.my_position, game_state)))

        action = self.action_coefficient(game_state, najwyzszy_wsp_pol)
        if action is not None:
            return action
        if dirs is None:
            return Pass()
        if len(dirs) < 2:
            return Pass()


        if dirs[1] == 'e':
            return Rotation(RotationDirection.RIGHT, RotationDirection.RIGHT)
        elif dirs[1] == 'q':
            return Rotation(RotationDirection.LEFT, RotationDirection.LEFT)
        else:
            return Movement(MovementDirection.FORWARD)


    def action_coefficient(self, game_state: GameState, best_tile):
        if self.secondary_item is SecondaryItemType.MINE:
            return AbilityUse(Ability.DROP_MINE)
        if self.secondary_item is SecondaryItemType.RADAR:
            return AbilityUse(Ability.USE_RADAR)
        if self.secondary_item is SecondaryItemType.LASER:
            d = get_turret_direction_of_player(self.my_position, game_state)
            pos = self.my_position
            x1, y1 = pos
            if d == Direction.UP:
                for x in range(self.my_position[0], 0, -1):
                    if self.pola[x][y1].is_wall:
                        break
                    if (x, y1) in self.enemies:
                        return AbilityUse(Ability.USE_LASER)
            if d == Direction.DOWN:
                for x in range(self.my_position[0], 21, 1):
                    if self.pola[x][y1].is_wall:
                        break
                    if (x, y1) in self.enemies:
                        return AbilityUse(Ability.USE_LASER)
            if d == Direction.LEFT:
                for y in range(self.my_position[0], 0, -1):
                    if self.pola[x1][y].is_wall:
                        break
                    if (x1, y) in self.enemies:
                        return AbilityUse(Ability.USE_LASER)
            if d == Direction.RIGHT:
                for y in range(self.my_position[0], 21, 1):
                    if self.pola[x1][y].is_wall:
                        break
                    if (x1, y) in self.enemies:
                        return AbilityUse(Ability.USE_LASER)
        if self.secondary_item is SecondaryItemType.DOUBLE_BULLET:
            d = get_turret_direction_of_player(self.my_position, game_state)
            pos = self.my_position
            x1, y1 = pos
            if d == Direction.UP:
                for x in range(self.my_position[0], 0, -1):
                    if self.pola[x][y1].is_wall:
                        break
                    if (x, y1) in self.enemies:
                        return AbilityUse(Ability.FIRE_DOUBLE_BULLET)
            if d == Direction.DOWN:
                for x in range(self.my_position[0], 21, 1):
                    if self.pola[x][y1].is_wall:
                        break
                    if (x, y1) in self.enemies:
                        return AbilityUse(Ability.FIRE_DOUBLE_BULLET)
            if d == Direction.LEFT:
                for y in range(self.my_position[0], 0, -1):
                    if self.pola[x1][y].is_wall:
                        break
                    if (x1, y) in self.enemies:
                        return AbilityUse(Ability.FIRE_DOUBLE_BULLET)
            if d == Direction.RIGHT:
                for y in range(self.my_position[0], 21, 1):
                    if self.pola[x1][y].is_wall:
                        break
                    if (x1, y) in self.enemies:
                        return AbilityUse(Ability.FIRE_DOUBLE_BULLET)
        if self.secondary_item is None or game_state.map.tiles[self.my_position[0]][self.my_position[1]].entities[0].turret.bullet_count > 0:
            d = get_turret_direction_of_player(self.my_position, game_state)
            pos = self.my_position
            x1, y1 = pos
            if d == Direction.UP:
                for x in range(self.my_position[0], 0, -1):
                    if self.pola[x][y1].is_wall:
                        break
                    if (x, y1) in self.enemies:
                        return AbilityUse(Ability.FIRE_BULLET)
            if d == Direction.DOWN:
                for x in range(self.my_position[0], 21, 1):
                    if self.pola[x][y1].is_wall:
                        break
                    if (x, y1) in self.enemies:
                        return AbilityUse(Ability.FIRE_BULLET)
            if d == Direction.LEFT:
                for y in range(self.my_position[0], 0, -1):
                    if self.pola[x1][y].is_wall:
                        break
                    if (x1, y) in self.enemies:
                        return AbilityUse(Ability.FIRE_BULLET)
            if d == Direction.RIGHT:
                for y in range(self.my_position[0], 21, 1):
                    if self.pola[x1][y].is_wall:
                        break
                    if (x1, y) in self.enemies:
                        return AbilityUse(Ability.FIRE_BULLET)

        return None



    def ruch_wiezy(self, gamestate):
        return rotation(get_rotation(self.my_position, find_closest_point(self.enemies, self.my_position)), get_turret_direction_of_player(self.my_position, gamestate))

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass

    def przelicz_wszystkie_wspolczyniki_pol(self, game_state):
        self.walkable = [[0 for _ in range(24)] for _ in range(24)]
        self.enemies = list()
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                contains_instance = False
                try:
                    contains_instance = any(isinstance(item, (Wall, Bullet, DoubleBullet, Laser, Mine, PlayerTank)) for item in game_state.map.tiles[poziom][pole].entities)
                except IndexError:
                    print("Index out of range for row:", poziom, "and column:", pole)
                    contains_instance = False
                if contains_instance:
                    self.walkable[poziom][pole] = 1
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
                    if isinstance(zone, NeutralZone):
                        self.pola[zone.y+i][zone.x+j].wsp += wsp_stref_neutral
                    elif isinstance(zone, BeingCapturedZone):
                        self.pola[zone.y+i][zone.x+j].wsp += wsp_stref_being_captured
                    elif isinstance(zone, CapturedZone):
                        self.pola[zone.y+i][zone.x+j].wsp += wsp_stref_captured
                    elif isinstance(zone, BeingContestedZone):
                        self.pola[zone.y+i][zone.x+j].wsp += wsp_stref_being_contested
                    elif isinstance(zone, BeingRetakenZone):
                        self.pola[zone.y+i][zone.x+j].wsp += wsp_stref_being_retaken

        obecny_wsp_podnoszenia = wsp_podnoszenia_przy_pelnym_ekwipunku
        ## zmiana współczynnika za każdy widziany element
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if self.pola[poziom][pole].is_wall:
                    continue
                if game_state.map.tiles[poziom][pole].is_visible:
                    ## wyjęcie wszystkich elementów z danego pola
                    for entity in game_state.map.tiles[poziom][pole].entities:
                        ## jeśli to wróg odejmujemy i patrzymy czy ma wieżę w naszą stornę
                        if isinstance(entity, PlayerTank):
                            if entity.owner_id != game_state.my_agent.id:
                                self.pola[poziom][pole].wsp += wsp_pola_z_wrogiem
                                ## jeśli go góry
                                if entity.turret.direction is Direction.UP:
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom - poziom_2 >= 0:
                                            if self.pola[poziom-poziom_2][pole].is_wall:
                                                break
                                            self.pola[poziom-poziom_2][pole].wsp += wsp_obserwowanego_pola
                                    for poziom_3 in range(len(self.pola)):
                                        if poziom + poziom_3 < len(self.pola):
                                            if self.pola[poziom+poziom_3][pole].is_wall:
                                                break
                                            self.pola[poziom+poziom_3][pole].wsp += wsp_nieobserwowanego_pola
                                            #print(poziom+poziom_2,pole,self.pola[poziom+poziom_2][pole].wsp)
                                    for pole_2 in range(len(self.pola)):
                                        if pole-pole_2 >= 0:
                                            if self.pola[poziom][pole-pole_2].is_wall:
                                                break
                                            self.pola[poziom][pole-pole_2].wsp += wsp_nieobserwowanego_pola/2
                                    for pole_3 in range(len(self.pola)):
                                        if pole + pole_3 < len(self.pola):
                                            if self.pola[poziom][pole+pole_3].is_wall:
                                                break
                                            self.pola[poziom][pole+pole_3].wsp += wsp_nieobserwowanego_pola/2
                                ## jeśli w dół
                                elif entity.turret.direction is Direction.DOWN:
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom_2 + poziom < len(self.pola):
                                            if self.pola[poziom+poziom_2][pole].is_wall:
                                                break
                                            self.pola[poziom+poziom_2][pole].wsp += wsp_obserwowanego_pola
                                            #print(poziom+poziom_2,pole,self.pola[poziom+poziom_2][pole].wsp)
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom - poziom_2 > 0:
                                            if self.pola[poziom-poziom_2][pole].is_wall:
                                                break
                                            self.pola[poziom-poziom_2][pole].wsp += wsp_nieobserwowanego_pola
                                    for pole_2 in range(len(self.pola)):
                                        if pole-pole_2 >= 0:
                                            if self.pola[poziom][pole-pole_2].is_wall:
                                                break
                                            self.pola[poziom][pole-pole_2].wsp += wsp_nieobserwowanego_pola/2
                                    for pole_2 in range(len(self.pola)):
                                        if pole + pole_2 < len(self.pola):
                                            if self.pola[poziom][pole+pole_2].is_wall:
                                                break
                                            self.pola[poziom][pole+pole_2].wsp += wsp_nieobserwowanego_pola/2
                                ## jeśli w lewo
                                elif entity.turret.direction is Direction.LEFT:
                                    for pole_2 in range(len(self.pola)):
                                        if pole-pole_2 >= 0:
                                            if self.pola[poziom][pole-pole_2].is_wall:
                                                break
                                            self.pola[poziom][pole-pole_2].wsp += wsp_obserwowanego_pola
                                    for pole_2 in range(len(self.pola)):
                                        if pole + pole_2 < len(self.pola):
                                            if self.pola[poziom][pole+pole_2].is_wall:
                                                break
                                            self.pola[poziom][pole+pole_2].wsp += wsp_nieobserwowanego_pola
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom_2 + poziom < len(self.pola):
                                            if self.pola[poziom+poziom_2][pole].is_wall:
                                                break
                                            self.pola[poziom+poziom_2][pole].wsp += wsp_nieobserwowanego_pola/2
                                            #print(poziom+poziom_2,pole,self.pola[poziom+poziom_2][pole].wsp)
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom - poziom_2 > 0:
                                            if self.pola[poziom-poziom_2][pole].is_wall:
                                                break
                                            self.pola[poziom-poziom_2][pole].wsp += wsp_nieobserwowanego_pola/2
                                ## jeśli w prawo
                                elif entity.turret.direction is Direction.RIGHT:
                                    for pole_2 in range(len(self.pola)):
                                        if pole_2 + pole < len(self.pola):
                                            if self.pola[poziom][pole+pole_2].is_wall:
                                                break
                                            self.pola[poziom][pole+pole_2].wsp += wsp_obserwowanego_pola
                                            #print(poziom,pole+pole_2,self.pola[poziom][pole+pole_2].wsp)
                                    for pole_2 in range(len(self.pola)):
                                        if pole - pole_2 > 0:
                                            if self.pola[poziom][pole-pole_2].is_wall:
                                                break
                                            self.pola[poziom][pole-pole_2].wsp += wsp_nieobserwowanego_pola
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom_2 + poziom < len(self.pola):
                                            if self.pola[poziom+poziom_2][pole].is_wall:
                                                break
                                            self.pola[poziom+poziom_2][pole].wsp += wsp_nieobserwowanego_pola/2
                                            #print(poziom+poziom_2,pole,self.pola[poziom+poziom_2][pole].wsp)
                                    for poziom_2 in range(len(self.pola)):
                                        if poziom - poziom_2 > 0:
                                            if self.pola[poziom-poziom_2][pole].is_wall:
                                                break
                                            self.pola[poziom-poziom_2][pole].wsp += wsp_nieobserwowanego_pola/2
                        #jeśli nie mamy itema ustawiamy wsp podnoszenia na 1
                        elif isinstance(entity, AgentTank):
                            self.pola[poziom][pole].wsp += wsp_pod_graczem
                            if entity.secondary_item is None:
                                obecny_wsp_podnoszenia = 1
                        # jeśli jest itemem dodajemy wsp mnożony przez współczynnik podnoszenia
                        elif isinstance(entity, Item):
                            #print("test", entity.type)
                            if entity.type == ItemType.LASER:
                                self.pola[poziom][pole].wsp += wsp_item_laser*obecny_wsp_podnoszenia
                            if entity.type == ItemType.DOUBLE_BULLET:
                                self.pola[poziom][pole].wsp += wsp_item_double_bullet*obecny_wsp_podnoszenia
                            if entity.type == ItemType.MINE:
                                self.pola[poziom][pole].wsp += wsp_item_mine*obecny_wsp_podnoszenia
                            if entity.type == ItemType.RADAR:
                                #print(wsp_item_radar*obecny_wsp_podnoszenia)
                                self.pola[poziom][pole].wsp += wsp_item_radar*obecny_wsp_podnoszenia
                            if entity.type == ItemType.UNKNOWN:
                                self.pola[poziom][pole].wsp += wsp_item_unknown
                        ## jeśli jest jakimś rodzajem pocisku dodajemy ujemny współczynnik
                        elif isinstance(entity, DoubleBullet):
                            self.pola[poziom][pole].wsp += wsp_bullet
                        elif isinstance(entity, Bullet):
                            self.pola[poziom][pole].wsp += wsp_double_bullet
                        elif isinstance(entity, Laser):
                            self.pola[poziom][pole].wsp += wsp_laser
                        elif isinstance(entity, Mine):
                            self.pola[poziom][pole].wsp += wsp_mine

    def show_map(self):
        print("-------------------------------------")
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                if self.pola[poziom][pole].is_wall:
                    print("#", end='  ')
                else:
                    print(math.floor(self.pola[poziom][pole].wsp), end='  ')
            print()

    def aktualizuj_secondary_item(self, game_state):
        for entity in game_state.map.tiles[self.my_position[0]][self.my_position[1]].entities:
            if isinstance(entity, AgentTank):
                self.secondary_item = entity.secondary_item

    def sprawdz_czy_wlaczyc_rage(self, game_state: GameState):
        if game_state.my_agent.score/self.my_tick < wsp_min_score_per_tick_rage:
            self.rage = True



    def __init__(self):
        self.my_tick = 0
        self.rage = False
        self.secondary_item = None
        self.enemies = list()
        self.my_position = tuple()
        self.initialized_walls = False
        self.pola = [[0 for _ in range(24)] for _ in range(24)]
        self.walkable = [[0 for _ in range(24)] for _ in range(24)]
        self.counter = 0
        self.xv = 1
        self.yv = 1
        self.is_ok = False
        for poziom in range(len(self.pola)):
            for pole in range(len(self.pola[poziom])):
                self.pola[poziom][pole] = Pole(pole, poziom)
                self.pola[poziom][pole].wsp = 0


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
