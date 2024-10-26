"""A module that contains the protocols used in the library.

Some of the protocols contain weird attributes like __instancecheck_something__.
These are used to distinguish between different classes that have the same
data structure. This is necessary to enable isinstance() to be used with protocols.
To take advantage of this, the models should have the same weird attribute as the protocol.

Notes
-----
Protocols are used to provide type hints for the classes
in the game state, lobby data, and game result.
"""

from __future__ import annotations

from typing import Protocol, Sequence, TYPE_CHECKING, runtime_checkable

if TYPE_CHECKING:
    from hackathon_bot.enums import (
        BulletType,
        Direction,
        ItemType,
        Orientation,
        SecondaryItemType,
        ZoneStatus,
    )


# pylint: disable=too-few-public-methods
# pylint: disable=too-many-lines


__all__ = (
    "ServerSettings",
    "GameStatePlayer",
    "LobbyPlayer",
    "GameEndPlayer",
    "Agent",
    "PlayerTurret",
    "AgentTurret",
    "PlayerTank",
    "AgentTank",
    "Wall",
    "Bullet",
    "Laser",
    "DoubleBullet",
    "Mine",
    "Item",
    "Tile",
    "LobbyData",
    "Zone",
    "NeutralZone",
    "BeingCapturedZone",
    "CapturedZone",
    "BeingContestedZone",
    "BeingRetakenZone",
    "Map",
    "GameState",
    "GameResult",
)


class ServerSettings(Protocol):
    """Represents the server settings.

    Attributes
    ----------
    grid_dimension: :class:`int`
        The grid dimension.
    number_of_players: :class:`int`
        The number of players.
    seed: :class:`int`
        The seed of the game.
    ticks: :class:`int`
        The number of game ticks.
    broadcast_interval: :class:`int`
        The broadcast interval in miliseconds.
    eager_broadcast: :class:`bool`
        Whether to eager broadcast is enabled.
    version: :class:`str`
        The version of the server.
    """

    @property
    def grid_dimension(self) -> int:
        """The grid dimension."""

    @property
    def number_of_players(self) -> int:
        """The number of players."""

    @property
    def seed(self) -> int:
        """The seed of the game."""

    @property
    def ticks(self) -> int | None:
        """The number of game ticks.

        For example, if the number of ticks is 2000,
        and the broadcast interval is 50 milliseconds,
        the game will last for 100 seconds (2000 / (1000 / 50))

        If sandbox mode is enabled, this value is `None`.
        """

    @property
    def broadcast_interval(self) -> int:
        """The broadcast interval.

        The interval in milliseconds between
        each broadcast game state.
        """

    @property
    def sandbox(self) -> bool:
        """Whether the game is in sandbox mode."""

    @property
    def eager_broadcast(self) -> bool:
        """Whether eager broadcast is enabled.

        If `True`, the server will broadcast the game state
        immediately after all agents respond to the latest game state.

        If `False`, the server will broadcast the game state
        after the broadcast interval.

        This allows for a shorter waiting time for the next broadcast
        if all agents respond to the latest game state.

        As a **participant of Hackathon**, you can **ignore this**.
        """

    @property
    def match_name(self) -> str | None:
        """The name of the match."""

    @property
    def version(self) -> str:
        """The version of the server."""


class GameStatePlayer(Protocol):
    """Represents a player in the game.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    nickname: :class:`str`
        The nickname of the player.
    color: :class:`int`
        The color of the player in format `0xAABBGGRR`.
    ping: :class:`int`
        The ping of the player.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""

    @property
    def nickname(self) -> str:
        """The nickname of the player."""

    @property
    def color(self) -> int:
        """The color of the player in format `0xAABBGGRR`."""

    @property
    def ping(self) -> int:
        """The ping of the player."""


class LobbyPlayer(Protocol):
    """Represents a player in the lobby.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    nickname: :class:`str`
        The nickname of the player.
    color: :class:`int`
        The color of the player in format `0xAABBGGRR`.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""

    @property
    def nickname(self) -> str:
        """The nickname of the player."""

    @property
    def color(self) -> int:
        """The color of the player in format `0xAABBGGRR`."""


class GameEndPlayer(Protocol):
    """Represents a player in the game result.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    nickname: :class:`str`
        The nickname of the player.
    color: :class:`int`
        The color of the player in format `0xAABBGGRR`.
    score: :class:`int`
        The score of the player.
    kills: :class:`int`
        The number of players killed by the player.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""

    @property
    def nickname(self) -> str:
        """The nickname of the player."""

    @property
    def color(self) -> int:
        """The color of the player in format `0xAABBGGRR`."""

    @property
    def score(self) -> int:
        """The score of the player."""

    @property
    def kills(self) -> int:
        """The number of players killed by the player."""


class Agent(GameStatePlayer, Protocol):
    """Represents your agent (player) in the game.

    Attributes
    ----------
    id: :class:`str`
        Your unique identifier.
    nickname: :class:`str`
        Your nickname.
    color: :class:`int`
        Your color in format `0xAABBGGRR`.
    score: :class:`int`
        Your score.
    ping: :class:`int`
        Your ping.
    ticks_to_regenerate: :class:`int` | `None`
        The number of ticks to regenerate your tank.
        If `None`, you are not dead.
    is_using_radar: :class:`bool`
        Whether you are using radar.
        If `True`, you see the whole map.
    """

    @property
    def id(self) -> str:
        """Your unique identifier."""

    @property
    def nickname(self) -> str:
        """Your nickname."""

    @property
    def color(self) -> int:
        """Your color in format `0xAABBGGRR`."""

    @property
    def score(self) -> int:
        """Your score."""

    @property
    def ticks_to_regenerate(self) -> int | None:
        """The number of ticks to regenerate your tank.

        If `None`, you are not dead.
        """

    @property
    def is_dead(self) -> bool:
        """Whether you are dead."""

    @property
    def is_using_radar(self) -> bool:
        """Whether you are using radar.

        If `True`, you see the whole map.
        """


class PlayerTurret(Protocol):
    """Represents a turret of a player's tank.

    Attributes
    ----------
    direction: :class:`Direction`
        The direction of the turret.
    """

    @property
    def direction(self) -> Direction:
        """The direction of the turret."""


class AgentTurret(Protocol):
    """Represents a turret of your agent's tank.

    Attributes
    ----------
    direction: :class:`Direction`
        The direction of the turret.
    bullet_count: :class:`int`
        The number of bullets in the turret.
    ticks_to_regenerate_bullet: :class:`int` | `None`
        The number of ticks to regenerate a bullet.
        If `None`, the turret has full bullets.
    """

    @property
    def direction(self) -> Direction:
        """The direction of your tank's turret."""

    @property
    def bullet_count(self) -> int:
        """The number of bullets in your tank's turret."""

    @property
    def ticks_to_regenerate_bullet(self) -> int | None:
        """The number of ticks to regenerate a bullet in your tank's turret.

        If `None`, your turret has full bullets.
        """


@runtime_checkable
class PlayerTank(Protocol):
    """Represents a tank of a player.

    Attributes
    ----------
    owner_id: :class:`str`
        The unique identifier of the owner.
    direction: :class:`Direction`
        The direction of the tank.
    turret: :class:`PlayerTurret`
        The turret of the tank.
    """

    __instancecheck_tank__: bool

    @property
    def owner_id(self) -> str:
        """The unique identifier of the owner."""

    @property
    def direction(self) -> Direction:
        """The direction of the tank."""

    @property
    def turret(self) -> PlayerTurret:
        """The turret of the tank."""


@runtime_checkable
class AgentTank(Protocol):
    """Represents a tank of your agent.

    Attributes
    ----------
    owner_id: :class:`str`
        Your unique identifier.
    direction: :class:`Direction`
        The direction of your tank.
    turret: :class:`AgentTurret`
        The turret of your tank.
    health: :class:`int` | `None`
        The health of your tank.
        If `None`, your tank is dead.
    secondary_item: :class:`int` | `None`
        The secondary item of your tank.
        If `None`, your tank does not have a secondary item.
    """

    __instancecheck_tank__: bool
    __instancecheck_agenttank__: bool

    @property
    def owner_id(self) -> str:
        """Your unique identifier."""

    @property
    def direction(self) -> Direction:
        """The direction of your tank."""

    @property
    def turret(self) -> AgentTurret:
        """The turret of your tank."""

    @property
    def health(self) -> int | None:
        """The health of your tank.

        If `None`, your tank is dead.
        """

    @property
    def secondary_item(self) -> SecondaryItemType | None:
        """The secondary item of your tank.

        If `None`, your tank does not have a secondary item.
        """


@runtime_checkable
class Wall(Protocol):
    """Represents a wall in the game.

    The wall does not have any attributes."""

    __instancecheck_wall__: bool


@runtime_checkable
class Bullet(Protocol):
    """Represents a bullet in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the bullet.
    speed: :class:`float`
        The speed of the bullet.
    direction: :class:`Direction`
        The direction of the bullet.
    type: :class:`BulletType`
        The type of the bullet.
    """

    __instancecheck_bullet__: bool

    @property
    def id(self) -> int:
        """The unique identifier of the bullet."""

    @property
    def speed(self) -> float:
        """The speed of the bullet."""

    @property
    def direction(self) -> Direction:
        """The direction of the bullet."""

    @property
    def type(self) -> BulletType:
        """The type of the bullet."""


@runtime_checkable
class Laser(Protocol):
    """Represents a laser in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the laser.
    orientation: :class:`Orientation`
        The orientation of the laser.
    """

    __instancecheck_laser__: bool

    @property
    def id(self) -> int:
        """The unique identifier of the laser."""

    @property
    def orientation(self) -> Orientation:
        """The orientation of the laser."""


@runtime_checkable
class DoubleBullet(Protocol):
    """Represents a double bullet in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the bullet.
    speed: :class:`float`
        The speed of the bullet.
    direction: :class:`Direction`
        The direction of the bullet.
    """

    __instancecheck_bullet__: bool
    __instancecheck_doublebullet__: bool

    @property
    def id(self) -> int:
        """The unique identifier of the double bullet."""

    @property
    def speed(self) -> float:
        """The speed of the double bullet."""

    @property
    def direction(self) -> Direction:
        """The direction of the double bullet."""


@runtime_checkable
class Mine(Protocol):
    """Represents a mine in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the mine.
    explosion_remaining_ticks: :class:`int`
        The remaining ticks to animate the mine explosion.
    exploded: :class:`bool`
        Whether the mine has exploded.
    """

    __instancecheck_mine__: bool

    @property
    def id(self) -> int:
        """The unique identifier of the mine."""

    @property
    def explosion_remaining_ticks(self) -> int | None:
        """The remaining ticks to animate the mine explosion.

        This value is mainly used for visualization purposes,
        but you can use it if you have a strategy that depends on it.

        Take note that the mine explodes immediately after
        a tank enters the tile containing the mine.
        Then the remaining ticks start counting down.

        If `None`, the mine has not exploded yet.
        """

    @property
    def exploded(self) -> bool:
        """Whether the mine has exploded.

        If `True`, the mine has exploded
        and only the explosion animation is visible.
        You can enter the tile containing the mine safely.
        """


@runtime_checkable
class Item(Protocol):
    """Represents a secondary item on the tile, that can be picked up by a tank.

    Item cannot be picked up if the tank already has a secondary item in its inventory.

    If a tank or mine is in the same tile as the item, the item type is unknown.

    Attributes
    ----------
    type: :class:`ItemType`
        The type of the item.
    """

    __instancecheck_item__: bool

    @property
    def type(self) -> ItemType:
        """The type of the item.

        The item can be one of the following types:
        - :class:`ItemType.UNKNOWN`
        - :class:`ItemType.LASER`
        - :class:`ItemType.DOUBLE_BULLET`
        - :class:`ItemType.RADAR`
        - :class:`ItemType.MINE`

        The item type is unknown if a tank or mine
        is in the same tile as the item.
        """


class LobbyData(Protocol):
    """Represents the lobby data.

    Attributes
    ----------
    my_id: :class:`str`
        Your unique identifier.
    players: Sequence[:class:`LobbyPlayer`]
        The sequence of players in the lobby.
    server_settings: :class:`payloads.ServerSettings`
        The server settings.
    """

    @property
    def my_id(self) -> str:
        """Your unique identifier."""

    @property
    def players(self) -> Sequence[LobbyPlayer]:
        """The sequence of players in the lobby."""

    @property
    def server_settings(self) -> ServerSettings:
        """The server settings."""


class Zone(Protocol):
    """Represents a zone in the game.

    The zone can be one of the following:
    - :class:`NeutralZone`
    - :class:`BeingCapturedZone`
    - :class:`CapturedZone`
    - :class:`BeingContestedZone`
    - :class:`BeingRetakenZone`

    There are two recommended ways to check the type of the zone:

    1. Using the `isinstance` function.

    ::

        if isinstance(zone, NeutralZone):
            # The zone is a neutral zone.
        elif isinstance(zone, BeingCapturedZone):
            # The zone is being captured.
            >>> zone.remaining_ticks  # Access the remaining ticks to capture the zone.
        # etc.

    2. Using the `status` attribute and casting the zone to the corresponding type.

    ::

        if zone.status is ZoneStatus.NEUTRAL:
            zone_neutral: NeutralZone = zone
        elif zone.status is ZoneStatus.BEING_CAPTURED:
            zone_being_captured: BeingCapturedZone = zone
            >> zone_being_captured.remaining_ticks  # Access the remaining ticks to capture the zone.
        # etc.

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    status: :class:`ZoneStatus`
        The status of the zone.
    """

    @property
    def x(self) -> int:
        """The x-coordinate of the zone."""

    @property
    def y(self) -> int:
        """The y-coordinate of the zone."""

    @property
    def width(self) -> int:
        """The width of the zone."""

    @property
    def height(self) -> int:
        """The height of the zone."""

    @property
    def index(self) -> int:
        """The index of the zone."""

    @property
    def status(self) -> ZoneStatus:
        """The status of the zone."""


@runtime_checkable
class NeutralZone(Zone, Protocol):
    """Represents a neutral zone in the game.

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    status: :class:`ZoneStatus`
        The status of the zone.
    """

    __instancecheck_neutralzone__: bool


@runtime_checkable
class BeingCapturedZone(Zone, Protocol):
    """Represents a zone being captured in the game.

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    status: :class:`ZoneStatus`
        The status of the zone.
    player_id: :class:`str`
        The unique identifier of the player capturing the zone.
    remaining_ticks: :class:`int`
        The remaining ticks to capture the zone.
    """

    __instancecheck_beingcapturedzone__: bool

    @property
    def player_id(self) -> str:
        """The unique identifier of the player capturing the zone."""

    @property
    def remaining_ticks(self) -> int:
        """The remaining ticks to capture the zone."""


@runtime_checkable
class CapturedZone(Zone, Protocol):
    """Represents a captured zone in the game.

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    status: :class:`ZoneStatus`
        The status of the zone.
    player_id: :class:`str`
        The unique identifier of the player capturing the zone.
    """

    __instancecheck_capturedzone__: bool

    @property
    def player_id(self) -> str:
        """The unique identifier of the player capturing the zone."""


@runtime_checkable
class BeingContestedZone(Zone, Protocol):
    """Represents a zone being contested in the game.

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    status: :class:`ZoneStatus`
        The status of the zone.
    captured_by_id: :class:`str` | `None`
        The unique identifier of the player capturing
        the zone if any. Otherwise, `None`.
    """

    __instancecheck_beingcontestedzone__: bool

    @property
    def captured_by_id(self) -> str | None:
        """The unique identifier of the player capturing the zone if any.

        Otherwise, `None`.
        """


@runtime_checkable
class BeingRetakenZone(Zone, Protocol):
    """Represents a zone being retaken in the game.

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    status: :class:`ZoneStatus`
        The status of the zone.
    captured_by_id: :class:`str`
        The unique identifier of the player capturing the zone.
    retaken_by_id: :class:`str`
        The unique identifier of the player retaking the zone.
    remaining_ticks: :class:`int`
        The remaining ticks to retake the zone.
    """

    __instancecheck_beingretakenzone__: bool

    @property
    def captured_by_id(self) -> str:
        """The unique identifier of the player capturing the zone."""

    @property
    def retaken_by_id(self) -> str:
        """The unique identifier of the player retaking the zone."""

    @property
    def remaining_ticks(self) -> int:
        """The remaining ticks to retake the zone."""


if TYPE_CHECKING:
    TileEntity = (
        PlayerTank | AgentTank | Wall | Bullet | Laser | DoubleBullet | Mine | Item
    )


class Tile(Protocol):
    """Represents a tile of the map.

    Attributes
    ----------
    entities: list[:class:`TileEntity`]
        The entities present on the tile.
    zone: :class:`Zone` | `None`
        The zone in the tile.
    is_visible: :class:`bool`
        Whether the tile is visible.
    """

    @property
    def entities(self) -> list[TileEntity]:
        """The entities present on the tile.

        The entity can be one of the following types:
        - :class:`Wall`
        - :class:`Bullet`
        - :class:`Laser`
        - :class:`DoubleBullet` *(see the important notes below)*
        - :class:`Mine`
        - :class:`Item`
        - :class:`PlayerTank`
        - :class:`AgentTank` *(see the important notes below)*

        Examples
        --------

        To check the type of the entity in the tile,
        use the `isinstance` function.

        ::

            for entity in tile.entities:
                if isinstance(entity, Wall):
                    # The entity is a wall.
                elif isinstance(entity, Bullet):
                    # The entity is a bullet.
                    # Warning: This includes both bullet and double bullet.
                    # See the important notes below.
                elif isinstance(entity, Mine):
                    # The entity is a mine.
                elif isinstance(entity, Item):
                    # The entity is an item.
                elif isinstance(entity, PlayerTank):
                    # The entity is a tank.
                    # Warning: This includes both your agent's tank and other player tanks.
                    # See the important notes below.

        If you have checked the type of the entity, you can easily access its attributes.

        ::

            for entity in tile.entities:
                if isinstance(entity, Mine):
                    >>> entity.exploded
                elif isinstance(entity, PlayerTank):
                    >>> entity.owner_id
                    >>> entity.direction
                    >>> entity.turret.direction

        Without checking the type of the entity, the linter may suggest
        all attributes of the entities in the tile, which can be misleading.


        Important Notes
        ---------------

        Be careful when distinguishing between your agent's tank and other player tanks
        or between bullet and double bullet.

        Since your agent's tank is also an instance of `PlayerTank`, and the `DoubleBullet` is
        also an instance of `Bullet`, it can be mistenly identified as the other type.

        For example:

        ::

            tile: Tile
            # Assume the first entity is your agent's tank
            entity_agent: AgentTank = tile.entities[0]
            # Assume the second entity is a double bullet
            entity_double_bullet: DoubleBullet = tile.entities[1]

            >>> isinstance(entity_agent, PlayerTank)  # True (!)
            >>> isinstance(entity_double_bullet, Bullet)  # True (!)

        To accurately distinguish between them, follow this pattern:

        ::

            if isinstance(entity_agent, AgentTank):
                # The entity is your agent's tank.
            elif isinstance(entity_agent, PlayerTank):
                # The entity is another player's tank.

            if isinstance(entity_double_bullet, DoubleBullet):
                # The entity is a double bullet.
            elif isinstance(entity_double_bullet, Bullet):
                # The entity is a bullet.

        Using `elif` ensures that only one condition is triggered, allowing you
        to differentiate between the two tank types properly.
        """

    @property
    def zone(self) -> Zone | None:
        """The zone in the tile.

        If the tile does not contain a zone,
        this property is `None`.
        """

    @property
    def is_visible(self) -> bool:
        """Whether the tile is visible
        from your agent's perspective.

        Note
        ----
        Using radar does not affect this property.
        The visibility of the tile is based on the
        line of sight of your agent's tank.
        """


class Map(Protocol):
    """Represents the map of the game state.

    Attributes
    ----------
    tiles: tuple[tuple[:class:`Tile`]]
        The tiles of the map in a 2D tuple,
        where the first index is the y-coordinate
        and the second index is the x-coordinate.
    zones: Sequence[:class:`Zone`]
        The zones on the map.
    """

    @property
    def tiles(self) -> tuple[tuple[Tile]]:
        """The tiles of the map in a 2D tuple.

        The first index is the y-coordinate
        and the second index is the x-coordinate.
        """

    @property
    def zones(self) -> tuple[Zone]:
        """The zones on the map."""


class GameState(Protocol):
    """Represents the game state.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the game state.
    tick: :class:`int`
        The tick of the game state.
    my_agent: :class:`Agent`
        Your agent in the game.
    players: Sequence[:class:`GameStatePlayer`]
        The sequence of players in the game state,
        including your agent.
    map: :class:`Map`
        The map of the game state.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the game state.

        This identifier is required by the server when
        sending the response payload of your action.
        This allows for a shorter waiting time for the next
        broadcast if all agents respond to the latest game state.

        As a **participant of Hackathon**, you can **ignore this**.
        Attaching the identifier to the response payload is done by
        this library automatically.
        """

    @property
    def tick(self) -> int:
        """The tick of the game state."""

    @property
    def my_agent(self) -> Agent:
        """Your agent in the game."""

    @property
    def players(self) -> Sequence[GameStatePlayer]:
        """The sequence of players in the game state,
        including your agent.
        """

    @property
    def map(self) -> Map:
        """The map of the game state."""


class GameResult(Protocol):
    """Represents the game result.

    Attributes
    ----------
    players: Sequence[:class:`GameEndPlayer`]
        The sequence of players in the game result.
    """

    @property
    def players(self) -> Sequence[GameEndPlayer]:
        """The sequence of players in the game result."""
