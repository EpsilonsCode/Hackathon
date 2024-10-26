"""A module that contains the payloads used in the library.

This module contains the payloads that are used to represent the data
that is sent and received between the client and the server.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import humps

# pylint: disable=too-many-instance-attributes


@dataclass(slots=True, frozen=True)
class ServerSettings:
    """Represents the server settings."""

    grid_dimension: int
    number_of_players: int
    seed: int
    ticks: int | None
    broadcast_interval: int
    sandbox_mode: bool
    eager_broadcast: bool
    match_name: str | None
    version: str


@dataclass(slots=True, frozen=True)
class RawPlayer:
    """Represents a raw player data."""

    id: str
    nickname: str
    color: int
    score: int | None = None
    kills: int | None = None
    ping: int | None = None
    ticks_to_regen: int | None = None
    is_using_radar: bool | None = None

    @classmethod
    def from_json(cls, json_data: dict) -> RawPlayer:
        """Creates a RawPlayer from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawMap:
    """Represents a raw map data."""

    tiles: tuple[tuple[tuple[RawTileObject] | None]]
    zones: tuple[RawZone]
    visibility: tuple[str]

    @classmethod
    def from_json(cls, json_data: dict) -> RawMap:
        """Creates a RawMap from a JSON dictionary."""

        json_data["tiles"] = tuple(
            tuple(tuple(RawTileObject.from_json(obj) for obj in tile) for tile in row)
            for row in json_data["tiles"]
        )
        json_data["zones"] = tuple(
            RawZone.from_json(zone) for zone in json_data["zones"]
        )
        json_data["visibility"] = tuple(json_data["visibility"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawTileObject:
    """Represents a raw tile object data."""

    type: str
    entity: RawTileEntity

    @classmethod
    def from_json(cls, json_data: dict) -> RawTileObject:
        """Creates a RawTileObject from a JSON dictionary."""

        obj_type = json_data.pop("type")

        payload_class_name = f"Raw{humps.pascalize(obj_type)}"
        payload_class = globals().get(payload_class_name)

        if payload_class is None or not issubclass(payload_class, RawTileEntity):
            raise ValueError(f"Unknown tile object class: {payload_class_name}")

        entity = payload_class.from_json(json_data.get("payload", {}))

        return cls(obj_type, entity)


@dataclass(slots=True, frozen=True)
class RawTileEntity(ABC):
    """Represents a raw tile entity data."""

    @classmethod
    @abstractmethod
    def from_json(cls, json_data: dict) -> RawTileEntity:
        """Creates a payload from a JSON dictionary."""


@dataclass(slots=True, frozen=True)
class RawWall(RawTileEntity):
    """Represents a raw wall data."""

    @classmethod
    def from_json(cls, json_data: dict) -> RawWall:
        """Creates a RawWall from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawBullet(RawTileEntity):
    """Represents a raw bullet data."""

    id: int
    speed: int | None
    direction: int | None
    type: int

    @classmethod
    def from_json(cls, json_data: dict) -> RawBullet:
        """Creates a RawBullet from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawLaser(RawTileEntity):
    """Represents a raw laser data."""

    id: int
    orientation: int

    @classmethod
    def from_json(cls, json_data: dict) -> RawLaser:
        """Creates a RawLaser from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawMine(RawTileEntity):
    """Represents a raw mine data."""

    id: int
    explosion_remaining_ticks: int | None = None

    @classmethod
    def from_json(cls, json_data: dict) -> RawMine:
        """Creates a RawMine from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawItem(RawTileEntity):
    """Represents a raw item data."""

    type: int

    @classmethod
    def from_json(cls, json_data: dict) -> RawItem:
        """Creates a RawItem from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawTank(RawTileEntity):
    """Represents a raw tank data."""

    owner_id: str
    direction: int
    turret: RawTurret
    health: int | None = None
    secondary_item: int | None = None

    @classmethod
    def from_json(cls, json_data: dict) -> RawTank:
        """Creates a RawTank from a JSON dictionary."""
        json_data["turret"] = RawTurret.from_json(json_data["turret"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawTurret:
    """Represents a raw turret data."""

    direction: int
    bullet_count: int | None = None
    ticks_to_regen_bullet: int | None = None

    @classmethod
    def from_json(cls, json_data: dict) -> RawTurret:
        """Creates a RawTurret from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawZone:
    """Represents a raw zone data."""

    x: int
    y: int
    width: int
    height: int
    index: int
    status: str
    player_id: str | None = None
    captured_by_id: str | None = None
    retaken_by_id: str | None = None
    remaining_ticks: int | None = None

    @classmethod
    def from_json(cls, json_data: dict) -> RawZone:
        """Creates a RawZone from a JSON dictionary."""
        status: dict = json_data.pop("status", {})
        json_data["status"] = status["type"]
        json_data["player_id"] = status.get("player_id", None)
        json_data["captured_by_id"] = status.get("captured_by_id", None)
        json_data["retaken_by_id"] = status.get("retaken_by_id", None)
        json_data["remaining_ticks"] = status.get("remaining_ticks", None)
        return cls(**json_data)


class Payload(ABC):  # pylint: disable=too-few-public-methods
    """Represents a payload that can be attached to a packet."""


@dataclass(slots=True, frozen=True)
class ConnectionRejectedPayload(Payload):
    """Represents a CONNECTION_REJECTED payload."""

    reason: str

    @classmethod
    def from_json(cls, json_data: dict) -> ConnectionRejectedPayload:
        """Creates a ConnectionRejectedPayload from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class LobbyDataPayload(Payload):
    """Represents a LOBBY_DATA payload."""

    player_id: str
    players: tuple[RawPlayer]
    server_settings: ServerSettings

    @classmethod
    def from_json(cls, json_data: dict) -> LobbyDataPayload:
        """Creates a LobbyDataPayload from a JSON dictionary."""
        json_data["players"] = tuple(
            RawPlayer.from_json(player) for player in json_data["players"]
        )
        json_data["server_settings"] = ServerSettings(**json_data["server_settings"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class GameStatePayload(Payload):
    """Represents a GAME_STATE payload."""

    id: str
    tick: int
    players: tuple[RawPlayer]
    map: RawMap

    @classmethod
    def from_json(cls, json_data: dict) -> GameStatePayload:
        """Creates a GameStatePayload from a JSON dictionary."""
        json_data["players"] = tuple(
            RawPlayer.from_json(player) for player in json_data["players"]
        )
        json_data["map"] = RawMap.from_json(json_data["map"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class GameEndPayload(Payload):
    """Represents a GAME_END payload."""

    players: tuple[RawPlayer]

    @classmethod
    def from_json(cls, json_data: dict) -> GameEndPayload:
        """Creates a GameEndPayload from a JSON dictionary."""
        json_data["players"] = tuple(
            RawPlayer(**player) for player in json_data["players"]
        )
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class ResponseActionPayload(Payload, ABC):
    """Represents a response action payload."""

    game_state_id: str


@dataclass(slots=True, frozen=True)
class MovementPayload(ResponseActionPayload):
    """Represents a MOVEMENT payload."""

    direction: int


@dataclass(slots=True, frozen=True)
class RotationPayload(ResponseActionPayload):
    """Represents a ROTATION payload."""

    tank_rotation: int | None
    turret_rotation: int | None


@dataclass(slots=True, frozen=True)
class AbilityUsePayload(ResponseActionPayload):
    """Represents an ABILITY_USE payload."""

    ability_type: int


@dataclass(slots=True, frozen=True)
class PassPayload(ResponseActionPayload):
    """Represents a PASS payload."""
