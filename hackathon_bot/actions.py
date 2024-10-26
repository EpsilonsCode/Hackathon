"""This module contains the response actions that the bot can take.

The response actions are used to define the bot's next move in the game.

Classes
-------
ResponseAction
    Base class for response actions.
Movement
    Represents a movement response action.
Rotation
    Represents a rotation response action.
AbilityUse
    Represents an ability use response action.
Pass
    Represents a pass response action.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, final

from .enums import (
    Ability,
    MovementDirection,
    PacketType,
    RotationDirection,
)
from .payloads import (
    ResponseActionPayload,
    MovementPayload,
    RotationPayload,
    AbilityUsePayload,
    PassPayload,
)


__all__ = (
    "ResponseAction",
    "Movement",
    "Rotation",
    "AbilityUse",
    "Pass",
)


@dataclass(slots=True, frozen=True)
class ResponseAction(ABC):
    """Base class for response actions."""

    packet_type: PacketType = field(init=False)

    @abstractmethod
    def to_payload(self, game_state_id: str) -> ResponseActionPayload:
        """Converts the response action to a payload."""


@dataclass(slots=True, frozen=True)
class Movement(ResponseAction):
    """Represents a movement response action.

    Example
    -------

    ::

        movement = Movement(MovementDirection.FORWARD)
    """

    movement_direction: MovementDirection
    packet_type: ClassVar[PacketType] = PacketType.MOVEMENT

    @final
    def to_payload(self, game_state_id: str) -> MovementPayload:
        return MovementPayload(game_state_id, self.movement_direction)


@dataclass(slots=True, frozen=True)
class Rotation(ResponseAction):
    """Represents a rotation response action.

    Example
    -------

    ::

        rotation = Rotation(RotationDirection.LEFT, RotationDirection.RIGHT)
    """

    tank_rotation_direction: RotationDirection | None
    turret_rotation_direction: RotationDirection | None
    packet_type: ClassVar[PacketType] = PacketType.ROTATION

    @final
    def to_payload(self, game_state_id: str) -> RotationPayload:
        return RotationPayload(
            game_state_id,
            self.tank_rotation_direction,
            self.turret_rotation_direction,
        )


@dataclass(slots=True, frozen=True)
class AbilityUse(ResponseAction):
    """Represents an ability use response action.

    Example
    -------

    ::

        # Fire bullet (basic attack)
        ability_use = AbilityUse(Ability.FIRE_BULLET)

        # Fire double bullet
        ability_use = AbilityUse(Ability.FIRE_DOUBLE_BULLET)

        # Use laser
        ability_use = AbilityUse(Ability.USE_LASER)

        # Use radar
        ability_use = AbilityUse(Ability.USE_RADAR)

        # Drop mine
        ability_use = AbilityUse(Ability.DROP_MINE)
    """

    ability: Ability
    packet_type: ClassVar[PacketType] = PacketType.ABILITY_USE

    @final
    def to_payload(self, game_state_id: str) -> AbilityUsePayload:
        return AbilityUsePayload(game_state_id, self.ability)


@dataclass(slots=True, frozen=True)
class Pass(ResponseAction):
    """Represents a pass response action.

    Example
    -------

    ::

        pass_ = Pass()
    """

    packet_type: ClassVar[PacketType] = PacketType.PASS

    @final
    def to_payload(self, game_state_id: str) -> AbilityUsePayload:
        return PassPayload(game_state_id)
