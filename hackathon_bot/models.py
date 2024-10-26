"""This module contains the models used in the library.

For streamlined versions with better documentation
and only essential fields, refer to the protocols
which serve as interfaces for these models with enhanced clarity.

Some of the models contain weird attributes like __instancecheck_something__.
These are used to distinguish between different classes that have the same
data structure. This is necessary to allow using isinstance() with protocols.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

import humps

from hackathon_bot.payloads import RawBullet, RawItem, RawLaser, RawMine

from .enums import BulletType, Direction, ItemType, Orientation, ZoneStatus

if TYPE_CHECKING:
    from .payloads import (
        GameStatePayload,
        GameEndPayload,
        LobbyDataPayload,
        RawMap,
        RawPlayer,
        RawTank,
        RawTurret,
        RawZone,
        ServerSettings,
    )


@dataclass(slots=True, frozen=True)
class PlayerModel:  # pylint: disable=too-many-instance-attributes
    """Represents a player model."""

    id: str
    nickname: str
    color: int
    score: int | None = None
    kills: int | None = None
    ping: int | None = None
    ticks_to_regenerate: int | None = None
    is_using_radar: bool | None = None

    @property
    def is_dead(self) -> bool:
        """Whether the player is dead."""
        return self.ticks_to_regenerate is not None

    @classmethod
    def from_raw(cls, raw: RawPlayer) -> PlayerModel:
        """Creates a player from a raw player payload."""
        data = asdict(raw)
        data["ticks_to_regenerate"] = data.pop("ticks_to_regen", None)
        return cls(**data)


@dataclass(slots=True, frozen=True)
class TurretModel:
    """Represents a turret model."""

    direction: Direction
    bullet_count: int | None = None
    ticks_to_regenerate_bullet: int | None = None

    @classmethod
    def from_raw(cls, raw: RawTurret) -> TurretModel:
        """Creates a turret from a raw turret payload."""
        data = asdict(raw)
        data["direction"] = Direction(data["direction"])
        data["ticks_to_regenerate_bullet"] = data.pop("ticks_to_regen_bullet", None)
        return cls(**data)


@dataclass(slots=True, frozen=True)
class TankModel:
    """Represents a tank model."""

    __instancecheck_tank__ = True

    owner_id: str
    direction: Direction
    turret: TurretModel
    health: int | None = None
    secondary_item: ItemType | None = None

    @classmethod
    def from_raw(cls, raw: RawTank) -> TankModel:
        """Creates a tank from a raw tank payload."""
        data = asdict(raw)
        data["direction"] = Direction(data["direction"])
        data["turret"] = TurretModel.from_raw(raw.turret)
        if raw.secondary_item is not None:
            data["secondary_item"] = ItemType(data["secondary_item"])
        return cls(**data)


@dataclass(slots=True, frozen=True)
class AgentTankModel(TankModel):
    """Represents an agent tank model."""

    __instancecheck_agenttank__ = True


@dataclass(slots=True, frozen=True)
class WallModel:
    """Represents a wall model."""

    __instancecheck_wall__ = True


@dataclass(slots=True, frozen=True)
class BulletModel:
    """Represents a bullet model."""

    __instancecheck_bullet__ = True

    id: int
    speed: float
    direction: Direction
    type: BulletType

    @classmethod
    def from_raw(cls, raw: RawBullet) -> BulletModel:
        """Creates a bullet from a raw bullet payload."""

        if raw.type == 1:  # Double
            return DoubleBulletModel.from_raw(raw)

        data = asdict(raw)
        data["direction"] = Direction(data["direction"])
        data["type"] = BulletType.BASIC
        return cls(**data)


@dataclass(slots=True, frozen=True)
class LaserModel:
    """Represents a laser model."""

    __instancecheck_laser__ = True

    id: int
    orientation: Orientation

    @classmethod
    def from_raw(cls, raw: RawLaser) -> LaserModel:
        """Creates a laser from a raw laser payload."""
        data = asdict(raw)
        data["orientation"] = Orientation(data["orientation"])
        return cls(**data)


@dataclass(slots=True, frozen=True)
class DoubleBulletModel(BulletModel):
    """Represents a double bullet model."""

    __instancecheck_doublebullet__ = True

    @classmethod
    def from_raw(cls, raw: RawBullet) -> DoubleBulletModel:
        """Creates a double bullet from a raw double bullet payload."""
        data = asdict(raw)
        data["type"] = BulletType.DOUBLE
        data["direction"] = Direction(data["direction"])
        return cls(**data)


@dataclass(slots=True, frozen=True)
class MineModel:
    """Represents a mine model."""

    __instancecheck_mine__ = True

    id: int
    explosion_remaining_ticks: int | None

    @property
    def exploded(self) -> bool:
        """Whether the mine has exploded."""
        return self.explosion_remaining_ticks is not None

    @classmethod
    def from_raw(cls, raw: RawMine) -> MineModel:
        """Creates a mine from a raw mine payload."""
        return cls(**asdict(raw))


@dataclass(slots=True, frozen=True)
class ItemModel:
    """Represents an item model."""

    __instancecheck_item__ = True

    type: ItemType

    @classmethod
    def from_raw(cls, raw: RawItem) -> ItemModel:
        """Creates an item from a raw item payload."""
        return cls(**asdict(raw))


@dataclass(slots=True, frozen=True)
class ZoneModel(ABC):  # pylint: disable=too-many-instance-attributes
    """Represents a zone model."""

    x: int
    y: int
    width: int
    height: int
    index: int
    status: ZoneStatus
    player_id: str | None = None
    captured_by_id: str | None = None
    retaken_by_id: str | None = None
    remaining_ticks: int | None = None

    @classmethod
    def from_raw(cls, raw: RawZone) -> ZoneModel:
        """Creates a zone from a raw zone payload."""
        data = asdict(raw)
        status = ZoneStatus(humps.decamelize(data["status"]).upper())
        data["status"] = status

        if status == ZoneStatus.NEUTRAL:
            zone = NeutralZoneModel
        elif status == ZoneStatus.BEING_CAPTURED:
            zone = BeingCapturedZoneModel
        elif status == ZoneStatus.CAPTURED:
            zone = CapturedZoneModel
        elif status == ZoneStatus.BEING_CONTESTED:
            zone = BeingContestedZoneModel
        elif status == ZoneStatus.BEING_RETAKEN:
            zone = BeingRetakenZoneModel
        else:
            raise ValueError(f"Unknown zone status: {status}")  # pragma: no cover

        return zone(**data)


@dataclass(slots=True, frozen=True)
class NeutralZoneModel(ZoneModel):
    """Represents a neutral zone model."""

    __instancecheck_neutralzone__ = True


@dataclass(slots=True, frozen=True)
class BeingCapturedZoneModel(ZoneModel):
    """Represents a zone model that is being captured."""

    __instancecheck_beingcapturedzone__ = True


@dataclass(slots=True, frozen=True)
class CapturedZoneModel(ZoneModel):
    """Represents a captured zone model."""

    __instancecheck_capturedzone__ = True


@dataclass(slots=True, frozen=True)
class BeingContestedZoneModel(ZoneModel):
    """Represents a zone model that is being contested."""

    __instancecheck_beingcontestedzone__ = True


@dataclass(slots=True, frozen=True)
class BeingRetakenZoneModel(ZoneModel):
    """Represents a zone model that is being retaken."""

    __instancecheck_beingretakenzone__ = True


@dataclass(slots=True, frozen=True)
class LobbyDataModel:
    """Represents the lobby data model."""

    player_id: str
    players: tuple[PlayerModel]
    server_settings: ServerSettings

    @property
    def my_id(self) -> str:
        """Your player ID."""
        return self.player_id

    @classmethod
    def from_payload(cls, payload: LobbyDataPayload) -> LobbyDataModel:
        """Creates a lobby data from a lobby data payload."""
        players = tuple(PlayerModel.from_raw(p) for p in payload.players)
        return cls(payload.player_id, players, payload.server_settings)


if TYPE_CHECKING:
    TileEntity = TankModel | WallModel | BulletModel


@dataclass(slots=True, frozen=True)
class TileModel:
    """Represents a tile model on the map."""

    entities: list[TileEntity]
    zone: ZoneModel | None
    is_visible: bool


@dataclass(slots=True, frozen=True)
class MapModel:
    """Represents a map model."""

    tiles: tuple[tuple[TileModel]]
    zones: tuple[ZoneModel]
    visibility: tuple[str]

    @classmethod
    def from_raw(  # pylint: disable=too-many-locals
        cls, raw: RawMap, agent_id: str
    ) -> MapModel:
        """Creates a map from a raw map payload."""
        zones = tuple(ZoneModel.from_raw(z) for z in raw.zones)

        tiles = []
        for x, row in enumerate(raw.tiles):
            tab = []
            for y, raw_tile in enumerate(row):
                objects = []
                for obj in raw_tile:
                    if obj.type == "tank":
                        raw_tank: RawTank = obj.entity
                        owner_id = raw_tank.owner_id
                        if owner_id == agent_id:
                            objects.append(AgentTankModel.from_raw(obj.entity))
                        else:
                            objects.append(TankModel.from_raw(obj.entity))
                    elif obj.type == "wall":
                        objects.append(WallModel())
                    elif obj.type == "bullet":
                        objects.append(BulletModel.from_raw(obj.entity))
                    elif obj.type == "laser":
                        objects.append(LaserModel.from_raw(obj.entity))
                    elif obj.type == "mine":
                        objects.append(MineModel.from_raw(obj.entity))
                    elif obj.type == "item":
                        objects.append(ItemModel.from_raw(obj.entity))
                    else:
                        raise ValueError(f"Unknown tile type: {obj.type}")

                is_visible = raw.visibility[y][x] == "1"
                zone = next(
                    (
                        z
                        for z in zones
                        if z.x <= x < z.x + z.width and z.y <= y < z.y + z.height
                    ),
                    None,
                )

                tab.append(TileModel(objects, zone, is_visible))
            tiles.append(tuple(tab))
        tiles = tuple(zip(*tiles))

        return MapModel(tuple(tiles), tuple(zones), raw.visibility)


@dataclass(slots=True, frozen=True)
class GameStateModel:
    """Represents a game state model."""

    id: str
    tick: int
    my_agent: PlayerModel
    players: tuple[PlayerModel]
    map: MapModel

    @classmethod
    def from_payload(cls, payload: GameStatePayload, agent_id: str) -> GameStateModel:
        """Creates a game state from a game state payload."""

        players = [PlayerModel.from_raw(p) for p in payload.players]
        agent = next(p for p in players if p.id == agent_id)

        return cls(
            id=payload.id,
            tick=payload.tick,
            my_agent=agent,
            players=players,
            map=MapModel.from_raw(payload.map, agent.id),
        )


@dataclass(slots=True, frozen=True)
class GameResultModel:
    """Represents the game results model."""

    players: tuple[PlayerModel]

    @classmethod
    def from_payload(cls, payload: GameEndPayload) -> GameResultModel:
        """Creates game results from a game end payload."""
        players = tuple(PlayerModel.from_raw(p) for p in payload.players)
        return cls(players)
