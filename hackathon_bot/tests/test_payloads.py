"""Tests for payloads module."""

import pytest

from hackathon_bot.payloads import (
    ConnectionRejectedPayload,
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
)

# pylint: disable=invalid-name


def test_RawPlayer_from_json__is_agent__is_not_dead():
    """Test RawPlayer.from_json method.

    The player is an agent and is not dead.
    """

    raw_player = RawPlayer.from_json(
        {
            "id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
            "nickname": "player1",
            "color": 4294901760,
            "ping": 4,
            "score": 23,
            "ticks_to_regen": None,
        }
    )

    assert raw_player.id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert raw_player.nickname == "player1"
    assert raw_player.color == 4294901760
    assert raw_player.ping == 4
    assert raw_player.score == 23
    assert raw_player.kills is None
    assert raw_player.ticks_to_regen is None


def test_RawPlayer_from_json__is_agent__is_dead():
    """Test RawPlayer.from_json method.

    The player is an agent and is dead.
    """

    raw_player = RawPlayer.from_json(
        {
            "id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
            "nickname": "player1",
            "color": 4294901760,
            "ping": 4,
            "score": 23,
            "ticks_to_regen": 22,
        }
    )

    assert raw_player.id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert raw_player.nickname == "player1"
    assert raw_player.color == 4294901760
    assert raw_player.ping == 4
    assert raw_player.score == 23
    assert raw_player.kills is None
    assert raw_player.ticks_to_regen == 22


def test_RawPlayer_from_json__is_not_agent():
    """Test RawPlayer.from_json method.

    The player is not an agent.
    """

    raw_player = RawPlayer.from_json(
        {
            "id": "e149e7a5-c849-4765-81be-c4538db33ecd",
            "nickname": "player2",
            "color": 4278190335,
            "ping": 1,
        }
    )

    assert raw_player.id == "e149e7a5-c849-4765-81be-c4538db33ecd"
    assert raw_player.nickname == "player2"
    assert raw_player.color == 4278190335
    assert raw_player.ping == 1
    assert raw_player.kills is None

    # The player is not an agent, so the following fields should be None.
    assert raw_player.score is None
    assert raw_player.ticks_to_regen is None


def test_RawTurret_from_json__player_is_agent__full_bullets():
    """Test RawTurret.from_json method.

    The player is an agent and has full bullets.
    """

    raw_turret = RawTurret.from_json(
        {"direction": 0, "bullet_count": 3, "ticks_to_regen_bullet": None}
    )

    assert raw_turret.direction == 0
    assert raw_turret.bullet_count == 3

    # The player has full bullets, so the following field should be None.
    assert raw_turret.ticks_to_regen_bullet is None


def test_RawTurret_from_json__player_is_agent__regenerating_bullet():
    """Test RawTurret.from_json method.

    The player is an agent and is regenerating a bullet.
    """

    raw_turret = RawTurret.from_json(
        {"direction": 0, "bullet_count": 2, "ticks_to_regen_bullet": 22}
    )

    assert raw_turret.direction == 0
    assert raw_turret.bullet_count == 2
    assert raw_turret.ticks_to_regen_bullet == 22


def test_RawTurret_from_json__player_is_not_agent():
    """Test RawTurret.from_json method.

    The player is not an agent.
    """

    raw_turret = RawTurret.from_json({"direction": 3})

    assert raw_turret.direction == 3

    # The player is not an agent, so the following fields should be None.
    assert raw_turret.bullet_count is None
    assert raw_turret.ticks_to_regen_bullet is None


def test_RawBullet_from_json__basic():
    """Test RawBullet.from_json method."""

    raw_bullet = RawBullet.from_json(
        {"id": 123, "speed": 2, "direction": 0, "type": "basic"}
    )

    assert raw_bullet.id == 123
    assert raw_bullet.speed == 2
    assert raw_bullet.direction == 0
    assert raw_bullet.type == "basic"


def test_RawBullet_from_json__double():
    """Test RawBullet.from_json method."""

    raw_bullet = RawBullet.from_json(
        {"id": 123, "speed": 2, "direction": 0, "type": "double"}
    )

    assert raw_bullet.id == 123
    assert raw_bullet.speed == 2
    assert raw_bullet.direction == 0
    assert raw_bullet.type == "double"


def test_RawLaser_from_json():
    """Test RawLaser.from_json method."""

    raw_laser = RawLaser.from_json({"id": 123, "orientation": 0})

    assert raw_laser.id == 123
    assert raw_laser.orientation == 0


def test_RawMine_from_json__not_exploding():
    """Test RawMine.from_json method.

    The mine is not exploding.
    """

    raw_mine = RawMine.from_json({"id": 123, "explosion_remaining_ticks": None})

    assert raw_mine.id == 123
    assert raw_mine.explosion_remaining_ticks is None


def test_RawMine_from_json__exploding():
    """Test RawMine.from_json method.

    The mine is exploding.
    """

    raw_mine = RawMine.from_json({"id": 123, "explosion_remaining_ticks": 10})

    assert raw_mine.id == 123
    assert raw_mine.explosion_remaining_ticks == 10


def test_RawItem_from_json():
    """Test RawItem.from_json method."""

    raw_item = RawItem.from_json({"type": 1})

    assert raw_item.type == 1


def test_RawWall_from_json():
    """Test RawWall.from_json method."""

    # Check if the method does not raise any exceptions.
    RawWall.from_json({})


def test_RawTank_from_json__player_is_agent():
    """Test RawTank.from_json method.

    The player is an agent.
    """

    raw_tank = RawTank.from_json(
        {
            "owner_id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
            "direction": 0,
            "turret": {
                "direction": 1,
                "bullet_count": 3,
                "ticks_to_regen_bullet": None,
            },
            "health": 100,
        }
    )

    assert raw_tank.owner_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert raw_tank.direction == 0
    assert isinstance(raw_tank.turret, RawTurret)
    assert raw_tank.health == 100


def test_RawTank_from_json__player_is_not_agent():
    """Test RawTank.from_json method.

    The player is not an agent.
    """
    raw_tank = RawTank.from_json(
        {
            "owner_id": "e149e7a5-c849-4765-81be-c4538db33ecd",
            "direction": 3,
            "turret": {"direction": 0},
        }
    )

    assert raw_tank.owner_id == "e149e7a5-c849-4765-81be-c4538db33ecd"
    assert raw_tank.direction == 3
    assert isinstance(raw_tank.turret, RawTurret)

    # The player is not an agent, so the health field should be None.
    assert raw_tank.health is None


zone_json_data_without_status = {
    "x": 0,
    "y": 0,
    "width": 2,
    "height": 2,
    "index": 65,
}


def test_RawZone_from_json():
    """Test RawZone.from_json method."""

    json_data = zone_json_data_without_status.copy()

    # The status is provided to avoid ValueError.
    # The status field is tested separately in other tests.
    json_data["status"] = {"type": "neutral"}
    raw_zone = RawZone.from_json(json_data)

    assert raw_zone.x == 0
    assert raw_zone.y == 0
    assert raw_zone.width == 2
    assert raw_zone.height == 2
    assert raw_zone.index == 65


def test_RawZone_from_json__neutral_status():
    """Test RawZone.from_json method with neutral status."""

    json_data = zone_json_data_without_status.copy()
    json_data["status"] = {"type": "neutral"}
    raw_zone = RawZone.from_json(json_data)

    assert raw_zone.status == "neutral"

    # Neutral status does not have the following fields.
    assert raw_zone.player_id is None
    assert raw_zone.captured_by_id is None
    assert raw_zone.retaken_by_id is None
    assert raw_zone.remaining_ticks is None


def test_RawZone_from_json__being_captured_status():
    """Test RawZone.from_json method with being_captured status."""

    json_data = zone_json_data_without_status.copy()
    json_data["status"] = {
        "type": "being_captured",
        "player_id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        "remaining_ticks": 10,
    }
    raw_zone = RawZone.from_json(json_data)

    assert raw_zone.status == "being_captured"
    assert raw_zone.player_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert raw_zone.remaining_ticks == 10

    # Being captured status does not have the following fields.
    assert raw_zone.captured_by_id is None
    assert raw_zone.retaken_by_id is None


def test_RawZone_from_json__captured_status():
    """Test RawZone.from_json method with captured status."""

    json_data = zone_json_data_without_status.copy()
    json_data["status"] = {
        "type": "captured",
        "captured_by_id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
    }

    raw_zone = RawZone.from_json(json_data)

    assert raw_zone.status == "captured"
    assert raw_zone.captured_by_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"

    # Captured status does not have the following fields.
    assert raw_zone.player_id is None
    assert raw_zone.retaken_by_id is None
    assert raw_zone.remaining_ticks is None


def test_RawZone_from_json__being_contested_status__not_captured():
    """Test RawZone.from_json method with being_contested status
    and the zone is not captured.
    """

    json_data = zone_json_data_without_status.copy()
    json_data["status"] = {
        "type": "being_contested",
        "captured_by_id": None,
    }
    raw_zone = RawZone.from_json(json_data)

    assert raw_zone.status == "being_contested"

    # The zone is not captured, so the following field should be None.
    assert raw_zone.captured_by_id is None

    # Being contested status does not have the following fields.
    assert raw_zone.player_id is None
    assert raw_zone.retaken_by_id is None
    assert raw_zone.remaining_ticks is None


def test_RawZone_from_json__being_contested_status__captured():
    """Test RawZone.from_json method with being_contested status
    and the zone is captured.
    """

    json_data = zone_json_data_without_status.copy()
    json_data["status"] = {
        "type": "being_contested",
        "captured_by_id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
    }
    raw_zone = RawZone.from_json(json_data)

    assert raw_zone.status == "being_contested"

    # The zone is captured, so the following field should be set.
    assert raw_zone.captured_by_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"

    # Being contested status does not have the following fields.
    assert raw_zone.player_id is None
    assert raw_zone.retaken_by_id is None
    assert raw_zone.remaining_ticks is None


def test_RawZone_from_json__being_retaken_status():
    """Test RawZone.from_json method with being_retaken status."""

    json_data = zone_json_data_without_status.copy()
    json_data["status"] = {
        "type": "being_retaken",
        "captured_by_id": "e149e7a5-c849-4765-81be-c4538db33ecd",
        "retaken_by_id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        "remaining_ticks": 10,
    }
    raw_zone = RawZone.from_json(json_data)

    assert raw_zone.status == "being_retaken"
    assert raw_zone.captured_by_id == "e149e7a5-c849-4765-81be-c4538db33ecd"
    assert raw_zone.retaken_by_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"
    assert raw_zone.remaining_ticks == 10

    # Being retaken status does not have the following field.
    assert raw_zone.player_id is None


def test_RawTileObject_from_json__wall():
    """Test RawTileObject.from_json method with wall type."""

    raw_tile_object = RawTileObject.from_json({"type": "wall"})

    # Check if the type is set correctly and the entity is an instance of RawWall.
    assert raw_tile_object.type == "wall"
    assert isinstance(raw_tile_object.entity, RawWall)


def test_RawTileObject_from_json__bullet():
    """Test RawTileObject.from_json method with bullet type."""

    raw_tile_object = RawTileObject.from_json(
        {
            "type": "bullet",
            "payload": {
                "id": 123,
                "speed": 2,
                "direction": 0,
                "type": "basic",
            },
        }
    )

    # Check if the type is set correctly and the entity is an instance of RawBullet.
    assert raw_tile_object.type == "bullet"
    assert isinstance(raw_tile_object.entity, RawBullet)


def test_RawTileObject_from_json__tank():
    """Test RawTileObject.from_json method with tank type."""

    raw_tile_object = RawTileObject.from_json(
        {
            "type": "tank",
            "payload": {
                "owner_id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
                "direction": 0,
                "turret": {
                    "direction": 1,
                },
            },
        }
    )

    # Check if the type is set correctly and the entity is an instance of RawTank.
    assert raw_tile_object.type == "tank"
    assert isinstance(raw_tile_object.entity, RawTank)


def test_RawTileObject_from_json__unknown_type():
    """Test RawTileObject.from_json method with unknown type.

    The method should raise ValueError."""

    with pytest.raises(ValueError):
        RawTileObject.from_json({"type": "unknown"})


def test_RawMap_from_json():
    """Test RawMap.from_json method."""

    raw_map = RawMap.from_json(
        {
            "tiles": [
                [
                    [{"type": "wall "}],
                    [],
                    [],
                ],
                [
                    [{"type": "wall "}],
                    [],
                    [],
                ],
                [
                    [],
                    [],
                    [],
                ],
            ],
            "zones": [
                {
                    "x": 0,
                    "y": 0,
                    "width": 2,
                    "height": 2,
                    "index": 65,
                    "status": {"type": "neutral"},
                }
            ],
            "visibility": ["110", "100", "000"],
        }
    )

    # Check if the tiles have been parsed correctly.
    assert len(raw_map.tiles) == 3
    assert isinstance(raw_map.tiles, tuple)
    for row in raw_map.tiles:
        assert isinstance(row, tuple)
        for tile in row:
            assert isinstance(tile, tuple)
            assert len(tile) <= 1
            for obj in tile:
                assert isinstance(obj, RawTileObject)

    # Check if the entities are parsed correctly.
    assert isinstance(raw_map.tiles[0][0][0].entity, RawWall)
    assert isinstance(raw_map.tiles[1][0][0], RawTileObject)
    assert len(raw_map.tiles[0][1]) == 0
    assert len(raw_map.tiles[1][0]) == 1, "Probably x and y coordinates are swapped"

    # Check if the zones have been parsed correctly.
    assert isinstance(raw_map.zones, tuple)
    assert isinstance(raw_map.zones[0], RawZone)

    # Check if the visibility has been parsed correctly.
    assert isinstance(raw_map.visibility, tuple)
    assert isinstance(raw_map.visibility[0], str)
    assert raw_map.visibility[0] == "110", "Probably x and y coordinates are swapped"


def test_ConnectionRejectedPayload():
    """Test ConnectionRejectedPayload.from_json method."""

    payload = ConnectionRejectedPayload.from_json({"reason": "rejection_reason"})
    assert payload.reason == "rejection_reason"


def test_LobbyDataPayload():
    """Test LobbyDataPayload.from_json method."""

    json_data = {
        "player_id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
        "players": [
            {
                "id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
                "nickname": "player1",
                "color": 4294901760,
            },
            {
                "id": "e149e7a5-c849-4765-81be-c4538db33ecd",
                "nickname": "player2",
                "color": 4278190335,
            },
        ],
        "server_settings": {
            "grid_dimension": 16,
            "number_of_players": 2,
            "seed": 42,
            "ticks": 1000,
            "broadcast_interval": 100,
            "sandbox_mode": False,
            "eager_broadcast": True,
            "match_name": None,
            "version": "v1.0.0"
        },
    }

    payload = LobbyDataPayload.from_json(json_data)

    # Check if the player_id is set correctly.
    assert payload.player_id == "7ed26efb-135d-4cd7-8bc7-c867a0b36d77"

    # Check if the players are a tuple of RawPlayer and have the correct length.
    assert isinstance(payload.players, tuple)
    assert len(payload.players) == 2
    assert all(isinstance(p, RawPlayer) for p in payload.players)

    # Check if the server settings are set correctly.
    assert payload.server_settings.grid_dimension == 16
    assert payload.server_settings.number_of_players == 2
    assert payload.server_settings.seed == 42
    assert payload.server_settings.ticks == 1000
    assert payload.server_settings.broadcast_interval == 100
    assert payload.server_settings.eager_broadcast is True


def test_GameStatePayload():
    """Test GameStatePayload.from_json method."""

    json_data = {
        "id": "0a0432fa-7fb1-42b9-8e85-7a1a085083a7",
        "tick": 42,
        "players": [
            {
                "id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
                "nickname": "player1",
                "color": 4294901760,
                "ping": 4,
                "score": 23,
                "ticks_to_regen": None,
            },
            {
                "id": "e149e7a5-c849-4765-81be-c4538db33ecd",
                "nickname": "player2",
                "color": 4278190335,
                "ping": 1,
            },
        ],
        "map": {
            "tiles": [[[{"type": "wall "}]]],
            "zones": [
                {
                    "x": 0,
                    "y": 0,
                    "width": 1,
                    "height": 1,
                    "index": 65,
                    "status": {"type": "neutral"},
                }
            ],
            "visibility": ["1"],
        },
    }

    payload = GameStatePayload.from_json(json_data)

    # Check if the id and tick are set correctly.
    assert payload.id == "0a0432fa-7fb1-42b9-8e85-7a1a085083a7"
    assert payload.tick == 42

    # Check if the players are a tuple of RawPlayer and have the correct length.
    assert isinstance(payload.players, tuple)
    assert len(payload.players) == 2
    assert all(isinstance(p, RawPlayer) for p in payload.players)

    # Check if the map is instance of RawMap.
    assert isinstance(payload.map, RawMap)

    # Check if the map tiles are set correctly.
    assert isinstance(payload.map.tiles, tuple)


def test_GameEndPayload():
    """Test GameEndPayload.from_json method."""

    json_data = {
        "players": [
            {
                "id": "7ed26efb-135d-4cd7-8bc7-c867a0b36d77",
                "nickname": "player1",
                "color": 4294901760,
                "score": 23,
                "kills": 5,
            },
            {
                "id": "e149e7a5-c849-4765-81be-c4538db33ecd",
                "nickname": "player2",
                "color": 4278190335,
                "score": 132,
                "kills": 2,
            },
        ],
    }

    payload = GameEndPayload.from_json(json_data)

    # Check if the players are a tuple of RawPlayer and have the correct length.
    assert isinstance(payload.players, tuple)
    assert len(payload.players) == 2
    assert all(isinstance(p, RawPlayer) for p in payload.players)
