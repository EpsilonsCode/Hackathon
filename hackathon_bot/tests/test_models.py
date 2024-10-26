"""Tests for models.py module."""

import pytest

from hackathon_bot.enums import BulletType, Direction, Orientation, ZoneStatus
from hackathon_bot.models import (
    BulletModel,
    ItemModel,
    LaserModel,
    MineModel,
    PlayerModel,
    TankModel,
    TurretModel,
    WallModel,
    ZoneModel,
    GameResultModel,
    GameStateModel,
    LobbyDataModel,
    MapModel,
    TileModel,
)
from hackathon_bot.payloads import (
    GameEndPayload,
    GameStatePayload,
    LobbyDataPayload,
    RawBullet,
    RawItem,
    RawLaser,
    RawMap,
    RawMine,
    RawPlayer,
    RawTank,
    RawTileObject,
    RawTurret,
    RawWall,
    RawZone,
    ServerSettings,
)

# pylint: disable=invalid-name


def test_Player_from_raw__game_state__is_agent__is_not_dead():
    """Test PlayerModel.from_raw method.

    The player is an agent and is not dead.
    """

    raw_player = RawPlayer(
        id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        nickname="player1",
        color=4294901760,
        score=23,
        ping=1,
        ticks_to_regen=None,
    )

    player = PlayerModel.from_raw(raw_player)

    assert player.id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert player.nickname == "player1"
    assert player.color == 4294901760
    assert player.score == 23
    assert player.ping == 1
    assert player.ticks_to_regenerate is None
    assert player.kills is None


def test_PlayerModel_from_raw__game_state__is_agent__is_dead():
    """Test PlayerModel.from_raw method.

    The player is an agent and is dead.
    """

    raw_player = RawPlayer(
        id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        nickname="player1",
        color=4294901760,
        score=23,
        ping=1,
        ticks_to_regen=22,
    )

    player = PlayerModel.from_raw(raw_player)

    assert player.id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert player.nickname == "player1"
    assert player.color == 4294901760
    assert player.score == 23
    assert player.ping == 1
    assert player.ticks_to_regenerate == 22
    assert player.kills is None


def test_PlayerModel_from_raw__game_state__is_not_agent():
    """Test PlayerModel.from_raw method.

    The player is not an agent.
    """

    raw_player = RawPlayer(
        id="e149e7a5-c849-4765-81be-c4538db33ecd",
        nickname="player2",
        color=4278190335,
        ping=1,
    )

    player = PlayerModel.from_raw(raw_player)

    assert player.id == "e149e7a5-c849-4765-81be-c4538db33ecd"
    assert player.nickname == "player2"
    assert player.color == 4278190335
    assert player.ping == 1

    # Player is not an agent, so the following attributes should be None.
    assert player.score is None
    assert player.kills is None
    assert player.ticks_to_regenerate is None


def test_PlayerModel_from_raw__lobby_data():
    """Test PlayerModel.from_raw method."""

    raw_player = RawPlayer(
        id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        nickname="player1",
        color=4278190335,
    )

    player = PlayerModel.from_raw(raw_player)

    assert player.id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert player.nickname == "player1"
    assert player.color == 4278190335

    # The following attributes should be None in the lobby data.
    assert player.score is None
    assert player.kills is None
    assert player.ping is None
    assert player.ticks_to_regenerate is None


def test_PlayerModel_from_raw__game_end():
    """Test PlayerModel.from_raw method."""

    raw_player = RawPlayer(
        id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        nickname="player1",
        color=4278190335,
        score=23,
        kills=2,
    )

    player = PlayerModel.from_raw(raw_player)

    assert player.id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert player.nickname == "player1"
    assert player.color == 4278190335
    assert player.score == 23
    assert player.kills == 2

    # The following attributes should be None in the game end data.
    assert player.ping is None
    assert player.ticks_to_regenerate is None


def test_TurretModel_from_raw__player_is_agent__full_bullets():
    """Test TurretModel.from_raw method.

    The player is an agent and has full bullets.
    """

    raw_turret = RawTurret(
        direction=Direction.UP,
        bullet_count=3,
        ticks_to_regen_bullet=None,
    )

    turret = TurretModel.from_raw(raw_turret)

    assert turret.direction == Direction.UP
    assert turret.bullet_count == 3
    assert turret.ticks_to_regenerate_bullet is None


def test_TurretModel_from_raw__player_is_agent__regenerating_bullets():
    """Test TurretModel.from_raw method.

    The player is an agent and is regenerating bullets.
    """

    raw_turret = RawTurret(
        direction=Direction.DOWN,
        bullet_count=2,
        ticks_to_regen_bullet=10,
    )

    turret = TurretModel.from_raw(raw_turret)

    assert turret.direction == Direction.DOWN
    assert turret.bullet_count == 2
    assert turret.ticks_to_regenerate_bullet == 10


def test_TurretModel_from_raw__player_is_not_agent():
    """Test TurretModel.from_raw method.

    The player is not an agent.
    """
    raw_turret = RawTurret(direction=Direction.LEFT)
    turret = TurretModel.from_raw(raw_turret)

    assert turret.direction == Direction.LEFT

    # The player is not an agent, so the following attributes should be None.
    assert turret.bullet_count is None
    assert turret.ticks_to_regenerate_bullet is None


def test_TankModel_from_raw__player_is_agent():
    """Test TankModel.from_raw method.

    The player is an agent.
    """

    raw_tank = RawTank(
        owner_id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        direction=Direction.RIGHT,
        turret=RawTurret(Direction.RIGHT, 2, 10),
        health=100,
    )

    tank = TankModel.from_raw(raw_tank)

    assert tank.owner_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert tank.direction == Direction.RIGHT
    assert isinstance(tank.turret, TurretModel)
    assert tank.health == 100


def test_TankModel_from_raw__player_is_not_agent():
    """Test TankModel.from_raw method.

    The player is not an agent.
    """

    raw_tank = RawTank(
        owner_id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        direction=Direction.LEFT,
        turret=RawTurret(Direction.LEFT),
    )

    tank = TankModel.from_raw(raw_tank)

    assert tank.owner_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert tank.direction == Direction.LEFT
    assert isinstance(tank.turret, TurretModel)

    # The player is not an agent, so the health attribute should be None.
    assert tank.health is None


def test_BulletModel_from_raw__basic():
    """Test BulletModel.from_raw method."""

    raw_bullet = RawBullet(123, 2, Direction.DOWN, "basic")
    bullet = BulletModel.from_raw(raw_bullet)

    assert bullet.id == 123
    assert bullet.speed == 2
    assert bullet.direction == Direction.DOWN
    assert bullet.type == BulletType.BASIC


def test_BulletModel_from_raw__double():
    """Test BulletModel.from_raw method."""

    raw_bullet = RawBullet(1233, 2, Direction.LEFT, 1)
    bullet = BulletModel.from_raw(raw_bullet)

    assert bullet.id == 1233
    assert bullet.speed == 2
    assert bullet.direction == Direction.LEFT
    assert bullet.direction is Direction.LEFT
    assert bullet.type == BulletType.DOUBLE
    assert bullet.type is BulletType.DOUBLE


def test_LaserModel_from_raw():
    """Test LaserModel.from_raw method."""

    raw_laser = RawLaser(123, 1)
    laser = LaserModel.from_raw(raw_laser)

    assert laser.id == 123
    assert laser.orientation == Orientation.VERTICAL
    assert laser.orientation is Orientation.VERTICAL


def test_MineModel_from_raw__not_exploding():
    """Test MineModel.from_raw method.

    The mine is not exploding.
    """

    raw_mine = RawMine(123, None)
    mine = MineModel.from_raw(raw_mine)

    assert mine.id == 123
    assert mine.explosion_remaining_ticks is None
    assert mine.exploded is False


def test_MineModel_from_raw__exploding():
    """Test MineModel.from_raw method.

    The mine is exploding.
    """

    raw_mine = RawMine(123, 10)
    mine = MineModel.from_raw(raw_mine)

    assert mine.id == 123
    assert mine.explosion_remaining_ticks == 10
    assert mine.exploded is True


def test_ItemModel_from_raw():
    """Test ItemModel.from_raw method."""

    raw_item = RawItem(1)
    item = ItemModel.from_raw(raw_item)

    assert item.type == 1


zone_json_data_without_status = {
    "x": 0,
    "y": 0,
    "width": 2,
    "height": 2,
    "index": 65,
}


def test_ZoneModel_from_raw():
    """Test ZoneModel.from_raw method."""

    # The status is provided to avoid the ValueError exception.
    # The status attribute is tested separately in other tests.
    raw_zone = RawZone(**zone_json_data_without_status, status="neutral")
    zone = ZoneModel.from_raw(raw_zone)

    assert zone.x == 0
    assert zone.y == 0
    assert zone.width == 2
    assert zone.height == 2
    assert zone.index == 65


def test_ZoneModel_from_raw__neutral_status():
    """Test ZoneModel.from_raw method with neutral status."""

    raw_zone = RawZone(**zone_json_data_without_status, status="neutral")
    zone = ZoneModel.from_raw(raw_zone)

    assert zone.status == ZoneStatus.NEUTRAL

    # The following attributes should be None when the zone is neutral.
    assert zone.player_id is None
    assert zone.captured_by_id is None
    assert zone.retaken_by_id is None
    assert zone.remaining_ticks is None


def test_ZoneModel_from_raw__being_captured_status():
    """Test ZoneModel.from_raw method with being_captured status."""

    raw_zone = RawZone(
        **zone_json_data_without_status,
        status="being_captured",
        player_id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        remaining_ticks=10,
    )

    zone = ZoneModel.from_raw(raw_zone)

    assert zone.status == ZoneStatus.BEING_CAPTURED
    assert zone.player_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert zone.remaining_ticks == 10

    # The following attributes should be None when the zone is being captured.
    assert zone.captured_by_id is None
    assert zone.retaken_by_id is None


def test_ZoneModel_from_raw__captured_status():
    """Test ZoneModel.from_raw method with captured status."""

    raw_zone = RawZone(
        **zone_json_data_without_status,
        status="captured",
        captured_by_id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
    )

    zone = ZoneModel.from_raw(raw_zone)

    assert zone.status == ZoneStatus.CAPTURED
    assert zone.captured_by_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"

    # The following attributes should be None when the zone is captured.
    assert zone.player_id is None
    assert zone.retaken_by_id is None
    assert zone.remaining_ticks is None


def test_ZoneModel_from_raw__being_retaken_status():
    """Test ZoneModel.from_raw method with being_retaken status."""

    raw_zone = RawZone(
        **zone_json_data_without_status,
        status="being_retaken",
        player_id=None,
        captured_by_id="e149e7a5-c849-4765-81be-c4538db33ecd",
        retaken_by_id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        remaining_ticks=22,
    )

    zone = ZoneModel.from_raw(raw_zone)

    assert zone.status == ZoneStatus.BEING_RETAKEN
    assert zone.captured_by_id == "e149e7a5-c849-4765-81be-c4538db33ecd"
    assert zone.retaken_by_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert zone.remaining_ticks == 22

    # The following attribute should be None when the zone is being retaken.
    assert zone.player_id is None


def test_ZoneModel_from_raw__being_contested_status__not_captured():
    """Test ZoneModel.from_raw method with being_contested status and not captured."""

    raw_zone = RawZone(
        **zone_json_data_without_status,
        status="being_contested",
        player_id=None,
        captured_by_id=None,
    )

    zone = ZoneModel.from_raw(raw_zone)

    assert zone.status == ZoneStatus.BEING_CONTESTED
    assert zone.captured_by_id is None

    # The following attributes should be None when the zone is being contested.
    assert zone.player_id is None
    assert zone.retaken_by_id is None
    assert zone.remaining_ticks is None


def test_ZoneModel_from_raw__being_contested_status__captured():
    """Test ZoneModel.from_raw method with being_contested status and captured."""

    raw_zone = RawZone(
        **zone_json_data_without_status,
        status="being_contested",
        player_id=None,
        captured_by_id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
    )

    zone = ZoneModel.from_raw(raw_zone)

    assert zone.status == ZoneStatus.BEING_CONTESTED
    assert zone.captured_by_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"

    # The following attributes should be None when the zone is being contested.
    assert zone.player_id is None
    assert zone.retaken_by_id is None
    assert zone.remaining_ticks is None


def test_LobbyData_from_payload():
    """Test LobbyDataModel.from_payload method."""

    lobby_data_payload = LobbyDataPayload(
        "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        [
            RawPlayer(
                id="7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
                nickname="player1",
                color=4278190335,
            ),
            RawPlayer(
                id="e149e7a5-c849-4765-81be-c4538db33ecd",
                nickname="player2",
                color=4278190335,
            ),
        ],
        ServerSettings(16, 2, 25319, 123, 100, False, True, None, "v1.0.0"),
    )

    lobby_data = LobbyDataModel.from_payload(lobby_data_payload)

    # Check if the player_id attribute is set correctly.
    assert lobby_data.player_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"

    # Check if the my_id attribute is the same as the player_id attribute.
    assert lobby_data.my_id == lobby_data.player_id

    # Check if all players are instances of PlayerModel.
    assert len(lobby_data.players) == 2
    assert all(isinstance(player, PlayerModel) for player in lobby_data.players)

    # Check if the server_settings attribute is an instance of ServerSettings.
    assert isinstance(lobby_data.server_settings, ServerSettings)


def test_Map_from_raw():
    """Test MapModel.from_raw method.

    The map has six tiles:
        ┌ ─ ┬ ─ ┬ ─ ┬ ─ ┐
        │ W │   │ A │ L │
        ├ ─ ┼ ─ ┼ ─ ┼ ─ ┤
        │ B │ T │M_T│ I │
        └ ─ ┴ ─ ┴ ─ ┴ ─ ┘
    Where:
        W - wall
        B - bullet
        T - tank
        A - agent tank
        M_T - mine and tank
        L - laser
        I - item

    The visibility of the tiles is as follows:
        ┌ ─ ┬ ─ ┬ ─ ┬ ─ ┐
        │ 1 │ 0 │ 1 │ 1 │
        ├ ─ ┼ ─ ┼ ─ ┼ ─ ┤
        │ 1 │ 1 │ 1 │ 1 │
        └ ─ ┴ ─ ┴ ─ ┴ ─ ┘

    The map has one zone with neutral status.
        ┌ ─ ┬ ─ ┬ ─ ┬ ─ ┐
        │ Z │ Z │   │   │
        ├ ─ ┼ ─ ┼ ─ ┼ ─ ┤
        │ Z │ Z │   │   │
        └ ─ ┴ ─ ┴ ─ ┴ ─ ┘
    """

    tiles = (
        (
            (RawTileObject("wall", RawWall()),),
            (RawTileObject("bullet", RawBullet(1, 2, Direction.UP, 0)),),
        ),
        (
            (()),
            (
                RawTileObject(
                    "tank",
                    RawTank(
                        "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
                        3,
                        RawTurret(3, 2, 10),
                        100,
                    ),
                ),
            ),
        ),
        (
            (
                RawTileObject(
                    "tank",
                    RawTank(
                        "e149e7a5-c849-4765-81be-c4538db33ecd",
                        3,
                        RawTurret(3),
                    ),
                ),
            ),
            (
                RawTileObject(
                    "tank",
                    RawTank(
                        "1af32fbs-1cvd-4164-8a13-vx67ab3s5623",
                        2,
                        RawTurret(2),
                    ),
                ),
                RawTileObject(
                    "mine",
                    RawMine(4, None),
                ),
            ),
        ),
        (
            (
                RawTileObject(
                    "laser",
                    RawLaser(555, 1),
                ),
            ),
            (
                RawTileObject(
                    "item",
                    RawItem(2),
                ),
            ),
        ),
    )

    visibility = ("1011", "1111")
    zones = (RawZone(**zone_json_data_without_status, status="neutral"),)
    raw_map = RawMap(tiles, zones, visibility)

    map_ = MapModel.from_raw(raw_map, "7ed26efb-135d-4cd7-8bc7-c867a0b36d77")

    # Check if the tiles attribute is a tuple of tuples of TileModel instances.
    assert isinstance(map_.tiles, tuple)
    assert all(isinstance(row, tuple) for row in map_.tiles)
    assert all(isinstance(tile, TileModel) for row in map_.tiles for tile in row)

    # Check if the tiles attribute contains the correct number of tiles.
    assert len(map_.tiles) == 2
    assert all(len(row) == 4 for row in map_.tiles)

    # Check if the is_visible attribute of the tiles is set correctly.
    assert map_.tiles[0][0].is_visible is True
    assert map_.tiles[1][0].is_visible is True
    assert map_.tiles[0][1].is_visible is False
    assert map_.tiles[1][1].is_visible is True
    assert map_.tiles[0][2].is_visible is True
    assert map_.tiles[1][2].is_visible is True
    assert map_.tiles[0][3].is_visible is True
    assert map_.tiles[1][3].is_visible is True

    # Check if the zone attribute of the tiles is set correctly.
    assert isinstance(map_.tiles[0][0].zone, ZoneModel)
    assert isinstance(map_.tiles[0][1].zone, ZoneModel)
    assert isinstance(map_.tiles[1][0].zone, ZoneModel)
    assert isinstance(map_.tiles[1][1].zone, ZoneModel)
    assert map_.tiles[0][2].zone is None
    assert map_.tiles[1][2].zone is None
    assert map_.tiles[0][3].zone is None
    assert map_.tiles[1][3].zone is None

    # Check if the entities of the tiles are set correctly.
    assert len(map_.tiles[0][0].entities) == 1
    assert isinstance(map_.tiles[0][0].entities[0], WallModel)

    assert len(map_.tiles[1][0].entities) == 1
    assert isinstance(map_.tiles[1][0].entities[0], BulletModel)

    assert len(map_.tiles[0][1].entities) == 0

    assert len(map_.tiles[1][1].entities) == 1
    assert isinstance(map_.tiles[1][1].entities[0], TankModel)

    assert len(map_.tiles[0][2].entities) == 1
    assert isinstance(map_.tiles[0][2].entities[0], TankModel)

    assert len(map_.tiles[1][2].entities) == 2
    assert isinstance(map_.tiles[1][2].entities[0], TankModel)
    assert isinstance(map_.tiles[1][2].entities[1], MineModel)

    assert len(map_.tiles[0][3].entities) == 1
    assert isinstance(map_.tiles[0][3].entities[0], LaserModel)

    assert len(map_.tiles[1][3].entities) == 1
    assert isinstance(map_.tiles[1][3].entities[0], ItemModel)

    # Check if the zones attribute is a tuple of ZoneModel instances
    # and has the correct length.
    assert isinstance(map_.zones, tuple)
    assert all(isinstance(zone, ZoneModel) for zone in map_.zones)
    assert len(map_.zones) == 1

    # Check if the visibility attribute is a tuple of strings and has the correct length.
    assert len(map_.visibility) == 2
    assert all(isinstance(v, str) for v in map_.visibility)


def test_Map_from_raw__unknown_tile_type():
    """Test MapModel.from_raw method with an unknown tile type.

    The method should raise a ValueError exception.
    """

    raw_map = RawMap(
        (((RawTileObject("unknown", None),),),),
        (()),
        ("1",),
    )

    with pytest.raises(ValueError):
        MapModel.from_raw(raw_map, "id")


def test_GameState_from_payload():
    """Test GameStateModel.from_payload method."""

    id_ = "0a0432fa-7fb1-42b9-8e85-7a1a085083a7"
    tick = 123
    players = (
        # Agent player
        RawPlayer(
            "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
            "player1",
            4278190335,
            23,
            1,
            22,
        ),
        # Non-agent player
        RawPlayer(
            "e149e7a5-c849-4765-81be-c4538db33ecd",
            "player2",
            4278190335,
        ),
    )
    map_ = RawMap(
        (((),),),
        (()),
        ("1",),
    )

    payload = GameStatePayload(id_, tick, players, map_)
    game_state = GameStateModel.from_payload(
        payload, "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    )

    # Check if the id and tick attributes are set correctly.
    assert game_state.id == "0a0432fa-7fb1-42b9-8e85-7a1a085083a7"
    assert game_state.tick == 123

    # Check if the players attribute is a tuple of PlayerModel
    # instances and has the correct length.
    assert len(game_state.players) == 2
    assert all(isinstance(player, PlayerModel) for player in game_state.players)

    # Check if the agent player is set correctly.
    assert isinstance(game_state.my_agent, PlayerModel)
    assert game_state.my_agent.id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"

    # Check if the map attribute is an instance of MapModel.
    assert isinstance(game_state.map, MapModel)


def test_GameResult_from_payload():
    """Test GameResultModel.from_payload method."""

    payload = GameEndPayload(
        (
            RawPlayer(
                "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
                "player1",
                4278190335,
                23,
            ),
            RawPlayer(
                "e149e7a5-c849-4765-81be-c4538db33ecd",
                "player2",
                4278190335,
                15,
            ),
        ),
    )

    game_result = GameResultModel.from_payload(payload)

    # Check if the players attribute is a tuple of PlayerModel
    # instances and has the correct length.
    assert len(game_result.players) == 2
    assert all(isinstance(player, PlayerModel) for player in game_result.players)
