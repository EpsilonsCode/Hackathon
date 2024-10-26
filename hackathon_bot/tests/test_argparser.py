"""Tests for the argparser module."""

import sys

import pytest
from hackathon_bot import argparser


def test_get_args(monkeypatch: pytest.MonkeyPatch):
    """Test get_args function."""

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--host",
            "localhost",
            "--port",
            "8080",
            "--code",
            "C0D3",
            "--nickname",
            "player1",
        ],
    )

    args = argparser.get_args()
    assert isinstance(args, argparser.Arguments)
    assert args.host == "localhost"
    assert args.port == 8080
    assert args.code == "C0D3"
    assert args.nickname == "player1"


def test_get_args__shortened(monkeypatch: pytest.MonkeyPatch):
    """Test get_args function with shortened arguments."""

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "-h",
            "localhost",
            "-p",
            "8080",
            "-c",
            "C0D3",
            "-n",
            "player1",
        ],
    )

    args = argparser.get_args()
    assert isinstance(args, argparser.Arguments)
    assert args.host == "localhost"
    assert args.port == 8080
    assert args.code == "C0D3"
    assert args.nickname == "player1"


def test_get_args__parse_error():
    """Test get_args function with parse error."""

    with pytest.raises(SystemExit):
        argparser.get_args()
