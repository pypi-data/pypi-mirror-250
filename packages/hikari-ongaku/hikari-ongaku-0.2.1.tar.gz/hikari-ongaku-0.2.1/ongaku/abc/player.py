import attrs
import typing as t

import hikari

from .track import Track
from .base import PayloadBase


@attrs.define
class PlayerState(PayloadBase):
    """
    Player State

    All of the Player State information.

    Find out more [here](https://lavalink.dev/api/websocket.html#player-state).

    Parameters
    ----------
    time : int
        Unix timestamp in milliseconds
    position : int
        The position of the track in milliseconds
    connected : bool
        Whether Lavalink is connected to the voice gateway
    ping : int
        The ping of the node to the Discord voice server in milliseconds (-1 if not connected)
    """

    time: int
    position: int
    connected: bool
    ping: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Player State parser

        parse a payload of information, to receive a `PlayerState` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlayerState
            The Player State you parsed.
        """
        time = payload["time"]
        position = payload["position"]
        connected = payload["connected"]
        ping = payload["ping"]

        return cls(time, position, connected, ping)


@attrs.define
class PlayerVoice(PayloadBase):
    """
    Player Voice

    All of the Player Voice information.

    Find out more [here](https://lavalink.dev/api/rest.html#voice-state).

    Parameters
    ----------
    token : str
        The Discord voice token to authenticate with
    endpoint : str
        The Discord voice endpoint to connect to
    session_id : str
        The Discord voice session id to authenticate with
    """

    token: str
    endpoint: str
    session_id: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Player Voice parser

        parse a payload of information, to receive a `PlayerVoice` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlayerVoice
            The Player Voice you parsed.
        """
        token = payload["token"]
        endpoint = payload["endpoint"]
        session_id = payload["sessionId"]

        return cls(token, endpoint, session_id)


@attrs.define
class Player(PayloadBase):
    """
    Player Voice

    All of the Player Voice information.

    Find out more [here](https://lavalink.dev/api/rest.html#player).

    Parameters
    ----------
    guild_id : hikari.Snowflake
        The guild id this player is currently in.
    track : abc.Track | None
        The track the player is currently playing. None means its not currently playing any track.
    volume : int
        The volume of the player.
    paused : int
        Whether the player is paused or not.
    state : PlayerState
        The `PlayerState` object
    voice : PlayerVoice
        The `PlayerVoice` object
    """

    guild_id: hikari.Snowflake
    track: t.Optional[Track]
    volume: int
    paused: bool
    state: PlayerState
    voice: PlayerVoice
    filters: dict[t.Any, t.Any] | None = None

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Player parser

        parse a payload of information, to receive a `Player` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Player
            The Player you parsed.
        """
        guild_id = hikari.Snowflake(payload["guildId"])
        try:
            track = Track.from_payload(payload["track"])
        except Exception:
            track = None
        volume = payload["volume"]
        paused = payload["paused"]
        state = PlayerState.as_payload(payload["state"])
        voice = PlayerVoice.as_payload(payload["voice"])
        filters = payload["filters"]

        return cls(guild_id, track, volume, paused, state, voice, filters)


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
