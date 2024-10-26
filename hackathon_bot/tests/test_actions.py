"""Tests for the actions module."""

import pytest
from hackathon_bot import (
    Movement,
    Rotation,
    AbilityUse,
    Pass,
    MovementDirection,
    RotationDirection,
)
from hackathon_bot.enums import Ability

# pylint: disable=invalid-name


@pytest.mark.parametrize(
    "direction", [MovementDirection.FORWARD, MovementDirection.BACKWARD]
)
def test_Movement_to_payload(direction):
    """Test Movement.to_payload method."""

    movement = Movement(direction)
    payload = movement.to_payload("game_state_id")

    assert payload.game_state_id == "game_state_id"
    assert payload.direction == direction


@pytest.mark.parametrize(
    "tank_rotation_direction, turret_rotation_direction",
    [
        (RotationDirection.LEFT, RotationDirection.LEFT),
        (RotationDirection.LEFT, RotationDirection.RIGHT),
        (RotationDirection.LEFT, None),
        (RotationDirection.RIGHT, RotationDirection.LEFT),
        (RotationDirection.RIGHT, RotationDirection.RIGHT),
        (RotationDirection.RIGHT, None),
        (None, RotationDirection.LEFT),
        (None, RotationDirection.RIGHT),
        (None, None),
    ],
)
def test_Rotation_to_payload(tank_rotation_direction, turret_rotation_direction):
    """Test Rotation.to_payload method."""

    rotation = Rotation(tank_rotation_direction, turret_rotation_direction)
    payload = rotation.to_payload("game_state_id")

    assert payload.game_state_id == "game_state_id"
    assert payload.tank_rotation == tank_rotation_direction
    assert payload.turret_rotation == turret_rotation_direction


@pytest.mark.parametrize("ability", tuple(Ability))
def test_AbilityUse_to_payload(ability):
    """Test Shoot.to_payload method."""

    shoot = AbilityUse(ability)
    payload = shoot.to_payload("game_state_id")

    assert payload.game_state_id == "game_state_id"
    assert payload.ability_type == ability


def test_Pass_to_payload():
    """Test Pass.to_payload method."""

    pass_ = Pass()
    payload = pass_.to_payload("game_state_id")

    assert payload.game_state_id == "game_state_id"
