"""Tests for the hackathon_bot module."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import ClassVar
from unittest.mock import AsyncMock, Mock, patch

import pytest
import websockets
import websockets.frames

from hackathon_bot import argparser
from hackathon_bot.actions import Pass, ResponseAction
from hackathon_bot.enums import PacketType, WarningType
from hackathon_bot.hackathon_bot import HackathonBot
from hackathon_bot.models import GameResultModel, GameStateModel, LobbyDataModel
from hackathon_bot.payloads import (
    GameEndPayload,
    GameStatePayload,
    LobbyDataPayload,
    Payload,
)
from hackathon_bot.protocols import GameResult, GameState, LobbyData

# pylint: disable=protected-access


@dataclass(slots=True, frozen=True)
class TestPayload(Payload):
    """Represents a test payload."""

    __test__ = False


@dataclass(slots=True, frozen=True)
class TestResponseAction(ResponseAction):
    """Represents a test response action."""

    __test__ = False

    packet_type: ClassVar[PacketType] = PacketType.UNKNOWN

    def to_payload(self, game_state_id: str) -> TestPayload:
        return TestPayload()


class TestBot(HackathonBot):  # pylint: disable=too-many-instance-attributes
    """Represents a test bot."""

    __test__ = False
    _loop = Mock()

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None: ...

    def next_move(self, game_state: GameState) -> ResponseAction: ...

    def on_game_ended(self, game_result: GameResult) -> None: ...

    def on_warning_received(
        self, warning: WarningType, message: str | None
    ) -> None: ...


def test_get_server_url() -> None:
    """Test _get_server_url method."""

    args = argparser.Arguments("localhost", 8080, "C0D3", "testBot")

    assert (
        TestBot()._get_server_url(args)
        == "ws://localhost:8080/?nickname=testBot&playerType=hackathonBot&joinCode=C0D3"
    )


@pytest.mark.asyncio
async def test_send_packet() -> None:
    """Test _send_packet method."""

    bot = TestBot()
    websocket = Mock()
    websocket.send = AsyncMock()

    await bot._send_packet(
        websocket,
        PacketType.UNKNOWN,
        TestPayload(),
    )

    websocket.send.assert_called_once()


class BaseTestWebsocket:
    """Represents a test websocket."""

    def __init__(self, url) -> None:
        pass

    async def __aenter__(self) -> BaseTestWebsocket:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass


class _TestWebsocketHandleMessages(BaseTestWebsocket):

    async def recv(self) -> str:
        """Simulate receiving a message."""

        # A small delay to simulate a real websocket connection.
        await asyncio.sleep(0.05)
        return json.dumps({"type": int(PacketType.UNKNOWN)})


class _TestWebsocketConnectionClosedOK(BaseTestWebsocket):

    async def recv(self) -> str:
        """Raise `ConnectionClosedOK` to exit the loop."""
        raise websockets.exceptions.ConnectionClosedOK(
            websockets.frames.Close(1000, "test"), None
        )


class _TestWebsocketConnectionClosedError(BaseTestWebsocket):

    async def recv(self) -> str:
        """Raise `ConnectionClosedError` to exit the loop."""
        raise websockets.exceptions.ConnectionClosedError(
            websockets.frames.Close(1001, "test"), None
        )


@pytest.mark.asyncio
async def test_start_loop() -> None:
    """Test _start_loop method."""

    bot = TestBot()
    bot._handle_messages = Mock()

    server_url = "ws://localhost:8080"

    with patch("websockets.connect", _TestWebsocketHandleMessages):
        try:
            await asyncio.wait_for(bot._start_loop(server_url), timeout=0.1)
        except asyncio.TimeoutError:
            pass

        assert bot._handle_messages.called


@pytest.mark.asyncio
async def test_start_loop_connection_closed_ok() -> None:
    """Test _start_loop method with ConnectionClosedOK exception."""

    bot = TestBot()
    bot._handle_messages = Mock()

    server_url = "ws://localhost:8080"

    with patch("websockets.connect", _TestWebsocketConnectionClosedOK):
        try:
            await asyncio.wait_for(bot._start_loop(server_url), timeout=0.1)
        except asyncio.TimeoutError:  # pragma: no cover
            # Loop should exit after receiving a ConnectionClosedOK exception.
            assert False  # pragma: no cover


@pytest.mark.asyncio
async def test_start_loop_connection_closed_error() -> None:
    """Test _start_loop method with ConnectionClosedError exception."""

    bot = TestBot()
    bot._handle_messages = Mock()

    server_url = "ws://localhost:8080"

    with patch("websockets.connect", _TestWebsocketConnectionClosedError):
        try:
            await asyncio.wait_for(bot._start_loop(server_url), timeout=0.1)
        except asyncio.TimeoutError:  # pragma: no cover
            # Loop should exit after receiving a ConnectionClosedError exception.
            assert False  # pragma: no cover


def test_run(monkeypatch):
    """Test run method."""

    mock_args = Mock()
    monkeypatch.setattr(argparser, "get_args", lambda: mock_args)

    mock_connection = AsyncMock()
    monkeypatch.setattr(websockets, "connect", AsyncMock(return_value=mock_connection))

    bot = TestBot()
    bot._get_server_url = Mock(return_value="ws://localhost:8080")
    bot._start_loop = AsyncMock(return_value=None)

    with patch("asyncio.run") as mock_run:
        mock_run.side_effect = asyncio.ensure_future
        bot.run()

        bot._get_server_url.assert_called_once_with(mock_args)
        bot._start_loop.assert_called_once_with("ws://localhost:8080")


def test_handle_messages__ping() -> None:
    """Test _handle_messages method with a ping packet."""

    ws = Mock()
    bot = TestBot()
    bot._handle_ping_packet = Mock()

    with patch.object(
        bot, "_handle_ping_packet", new_callable=Mock
    ) as mock_handle_ping:
        bot._handle_messages(ws, json.dumps({"type": PacketType.PING}))
        mock_handle_ping.assert_called_once_with(ws)


def test_handle_messages__game_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _handle_messages method with a game state packet."""

    ws = Mock()
    bot = TestBot()
    bot._lobby_data = Mock()
    bot._handle_next_move = Mock()

    game_state = Mock()

    monkeypatch.setattr(GameStatePayload, "from_json", Mock())
    monkeypatch.setattr(GameStateModel, "from_payload", Mock(return_value=game_state))

    # Check if the _handle_next_move method was called with the game state
    with patch.object(
        bot, "_handle_next_move", new_callable=Mock
    ) as mock_handle_game_state:
        bot._handle_messages(
            ws, json.dumps({"type": PacketType.GAME_STATE, "payload": {}})
        )
        mock_handle_game_state.assert_called_once_with(ws, game_state)


def test_handle_messages__lobby_data(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _handle_messages method with a lobby data packet."""

    ws = Mock()
    bot = TestBot()
    bot.on_lobby_data_received = Mock()

    lobby_data = Mock()

    monkeypatch.setattr(LobbyDataPayload, "from_json", Mock(return_value=TestPayload()))
    monkeypatch.setattr(LobbyDataModel, "from_payload", Mock(return_value=lobby_data))

    # Check if the on_lobby_data_received method was called with the lobby data
    with patch.object(
        bot, "on_lobby_data_received", new_callable=Mock
    ) as mock_handle_lobby_data:
        bot._handle_messages(
            ws, json.dumps({"type": PacketType.LOBBY_DATA, "payload": {}})
        )
        mock_handle_lobby_data.assert_called_once_with(lobby_data)

    # Check if the lobby data was set correctly
    assert bot._lobby_data == lobby_data


@pytest.mark.parametrize(
    "packet_type, message",
    [
        (PacketType.CUSTOM_WARNING, "custom_message"),
        (PacketType.PLAYER_ALREADY_MADE_ACTION_WARNING, None),
        (PacketType.SLOW_RESPONSE_WARNING, None),
        (PacketType.ACTION_IGNORED_DUE_TO_DEAD_WARNING, None),
    ],
)
def test_handle_messages__warning(packet_type, message) -> None:
    """Test _handle_messages method with a warning packet."""

    ws = Mock()
    bot = TestBot()
    bot.on_warning_received = Mock()

    # Check if the on_warning_received method was called with the warning and the message
    with patch.object(
        bot, "on_warning_received", new_callable=Mock
    ) as mock_handle_warning:
        bot._handle_messages(
            ws,
            json.dumps(
                {
                    "type": packet_type,
                    "payload": message,
                }
            ),
        )
        mock_handle_warning.assert_called_once_with(packet_type, message)


def test_handle_messages__error__with_message() -> None:
    """Test _handle_messages method with a warning packet."""

    ws = Mock()
    bot = TestBot()

    with patch("builtins.print") as mock_print:
        bot._handle_messages(
            ws,
            json.dumps(
                {"type": PacketType.ERROR_GROUP, "payload": {"message": "message"}}
            ),
        )

        mock_print.assert_called_once()


def test_handle_messages__error__without_message() -> None:
    """Test _handle_messages method with a warning packet."""

    ws = Mock()
    bot = TestBot()

    with patch("builtins.print") as mock_print:
        bot._handle_messages(
            ws,
            json.dumps({"type": PacketType.ERROR_GROUP, "payload": {}}),
        )

        mock_print.assert_called_once()


def test_handle_messages__connection_accepted() -> None:
    """Test _handle_messages method with a connection accepted packet."""

    bot = TestBot()
    ws = Mock()

    # Check if the method does not raise an exception
    bot._handle_messages(ws, json.dumps({"type": PacketType.CONNECTION_ACCEPTED}))


def test_handle_messages__game_in_progress() -> None:
    """Test _handle_messages method with a game status packet."""

    bot = TestBot()
    ws = Mock()
    bot.send_lobby_data_request = Mock()
    bot._send_ready_to_receive_game_state = Mock()

    bot._handle_messages(ws, json.dumps({"type": PacketType.GAME_IN_PROGRESS}))

    bot.send_lobby_data_request.assert_called_once_with(ws)
    bot._send_ready_to_receive_game_state.assert_called_once_with(ws)


def test_handle_messages__connection_rejected() -> None:
    """Test _handle_messages method with a connection rejected packet."""

    bot = TestBot()
    ws = Mock()

    # Check if the reason is printed
    with patch("builtins.print") as mock_print:
        bot._handle_messages(
            ws,
            json.dumps(
                {"type": PacketType.CONNECTION_REJECTED, "payload": {"reason": "test"}}
            ),
        )

        mock_print.assert_called_once_with("Connection rejected: test")


def test_handle_messages__game_started() -> None:
    """Test _handle_messages method with a game start packet."""

    bot = TestBot()
    ws = Mock()

    # Check if the method does not raise an exception
    bot._handle_messages(ws, json.dumps({"type": PacketType.GAME_STARTED}))


def test_handle_messages__game_starting__lobby_data_set() -> None:
    """Test _handle_messages method with a game starting packet."""

    bot = TestBot()
    ws = Mock()
    bot._lobby_data = Mock()
    bot.send_lobby_data_request = Mock()
    bot._send_ready_to_receive_game_state = Mock()

    bot._handle_messages(ws, json.dumps({"type": PacketType.GAME_STARTING}))

    bot.send_lobby_data_request.assert_not_called()
    bot._send_ready_to_receive_game_state.assert_called_once_with(ws)


def test_handle_messages__game_starting__lobby_data_not_set() -> None:
    """Test _handle_messages method with a game starting packet."""

    bot = TestBot()
    ws = Mock()
    bot._lobby_data = None
    bot.send_lobby_data_request = Mock()
    bot._send_ready_to_receive_game_state = Mock()

    bot._handle_messages(ws, json.dumps({"type": PacketType.GAME_STARTING}))

    bot.send_lobby_data_request.assert_called_once_with(ws)
    bot._send_ready_to_receive_game_state.assert_called_once_with(ws)


def test_handle_messages__game_ended(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _handle_messages method with a game end packet."""
    bot = TestBot()
    ws = Mock()

    game_result = Mock()

    monkeypatch.setattr(GameEndPayload, "from_json", Mock(return_value=TestPayload()))
    monkeypatch.setattr(GameResultModel, "from_payload", Mock(return_value=game_result))

    # Check if the on_game_ended method was called with the game result
    with patch.object(bot, "on_game_ended", new_callable=Mock) as mock_handle_game_end:
        bot._handle_messages(
            ws, json.dumps({"type": PacketType.GAME_ENDED, "payload": {}})
        )
        mock_handle_game_end.assert_called_once_with(game_result)


def test_handle_ping_packet() -> None:
    """Test _handle_ping_packet method."""

    ws = Mock()
    bot = TestBot()
    bot._send_packet = Mock()

    with patch("asyncio.run_coroutine_threadsafe") as mock_run_coroutine_threadsafe:
        bot._handle_ping_packet(ws)

        bot._send_packet.assert_called_once_with(ws, PacketType.PONG)
        mock_run_coroutine_threadsafe.assert_called_once()


def test_handle_next_move__is_processing():
    """Test _handle_next_move method when the bot is processing.

    The method should not call the next_move method.
    """

    bot = TestBot()
    bot._is_processing = True
    ws = Mock()

    bot.next_move = Mock()

    bot._handle_next_move(ws, TestPayload())

    bot.next_move.assert_not_called()


def test_handle_next_move__is_not_processing():
    """Test _handle_next_move method when the bot is not processing.

    The method should call the next_move method.
    After receiving the response action, the method
    should set the _is_processing flag to False and send a packet.
    """

    bot = TestBot()
    bot._is_processing = False
    ws = Mock()
    game_state = Mock()
    test_response_action = TestResponseAction()

    bot.next_move = Mock(return_value=test_response_action)
    bot._send_packet = Mock()

    with patch("asyncio.run_coroutine_threadsafe") as mock_run_coroutine_threadsafe:
        bot._handle_next_move(ws, game_state)

        # Check if the next_move method was called
        bot.next_move.assert_called_once_with(game_state)

        # Check if the _is_processing flag was set to False
        assert bot._is_processing is False

        # Check if the packet was sent
        mock_run_coroutine_threadsafe.assert_called_once()
        bot._send_packet.assert_called_once_with(
            ws,
            test_response_action.packet_type,
            test_response_action.to_payload(game_state.id),
        )


def test_handle_next_move__keyboard_interrupt():
    """Test _handle_next_move method when a KeyboardInterrupt is raised."""

    bot = TestBot()
    bot._is_processing = False
    ws = Mock()

    bot.next_move = Mock(side_effect=KeyboardInterrupt)

    with pytest.raises(KeyboardInterrupt):
        bot._handle_next_move(ws, Mock())


def test_handle_next_move__next_move_failed():
    """Test _handle_next_move method when
    the next_move method raises an exception.

    The method should print the error and
    set the _is_processing flag to False.
    """

    bot = TestBot()
    bot._is_processing = False
    ws = Mock()

    bot.next_move = Mock(side_effect=Exception)

    # Check if the error is printed
    with patch("builtins.print") as mock_print:
        bot._handle_next_move(ws, TestPayload())
        mock_print.assert_called()

    # Check if the next_move method was called
    bot.next_move.assert_called_once()

    # Check if the _is_processing flag was set to False
    assert bot._is_processing is False


def test_handle_next_move_pass():
    """Test _handle_next_move method when the next move returns `None`."""

    ws = AsyncMock()
    game_state = Mock()

    bot = TestBot()
    bot._is_processing = False
    bot.next_move = Mock(return_value=None)
    bot._send_packet = Mock()

    with patch("asyncio.run_coroutine_threadsafe") as mock_run_coroutine_threadsafe:
        bot._handle_next_move(ws, game_state)

        # Check if the next_move method was called
        bot.next_move.assert_called_once_with(game_state)

        # Check if the _is_processing flag was set to False
        assert bot._is_processing is False

        # Check if the packet was sent
        mock_run_coroutine_threadsafe.assert_called_once()
        payload = Pass().to_payload(game_state.id)
        bot._send_packet.assert_called_once_with(ws, Pass().packet_type, payload)


def test_send_ready_to_receive_game_state() -> None:
    """Test _send_ready_to_receive_game_state method."""

    ws = Mock()
    bot = TestBot()
    bot._send_packet = Mock()

    with patch("asyncio.run_coroutine_threadsafe") as mock_run_coroutine_threadsafe:
        bot._send_ready_to_receive_game_state(ws)

        bot._send_packet.assert_called_once_with(
            ws, PacketType.READY_TO_RECEIVE_GAME_STATE
        )
        mock_run_coroutine_threadsafe.assert_called_once()


def test_send_lobby_data_request() -> None:
    """Test _send_lobby_data_request method."""

    ws = Mock()
    bot = TestBot()
    bot._send_packet = Mock()

    with patch("asyncio.run_coroutine_threadsafe") as mock_run_coroutine_threadsafe:
        bot.send_lobby_data_request(ws)

        bot._send_packet.assert_called_once_with(ws, PacketType.LOBBY_DATA_REQUEST)
        mock_run_coroutine_threadsafe.assert_called_once()


def test_send_game_status_request() -> None:
    """Test _send_ready_lobby_data_request method."""

    ws = Mock()
    bot = TestBot()
    bot._send_packet = Mock()

    with patch("asyncio.run_coroutine_threadsafe") as mock_run_coroutine_threadsafe:
        bot._send_game_status_request(ws)

        bot._send_packet.assert_called_once_with(ws, PacketType.GAME_STATUS_REQUEST)
        mock_run_coroutine_threadsafe.assert_called_once()
