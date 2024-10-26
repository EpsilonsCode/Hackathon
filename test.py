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


import math


def find_closest_point(points, player):
    closest_point = None
    min_distance = float('inf')  # Initialize with a very large number

    for point in points:
        distance = math.sqrt((point[0] - player[0]) ** 2 + (point[1] - player[1]) ** 2)

        if distance < min_distance:
            min_distance = distance
            closest_point = point

    return closest_point


# Example usage
points_list = [(1, 2), (3, 4), (5, 1), (2, 3)]
special_point = (2, 2)

closest = find_closest_point(points_list, special_point)
print(closest)  # Output will be (1, 2) or (2, 3), depending on which is considered closer

# Example usage
entity_position = (0, 0)
reference_position = (0, 5)

direction = rotation(get_rotation(entity_position, reference_position), 'd')
print(direction)  # Output will be 'above'
print(get_rotation(entity_position, reference_position))