from unittest.mock import Mock

import pytest

from scripts.fetch import spotify_fetch


def test_import_does_not_create_a_spotify_client():
    assert not hasattr(spotify_fetch, "sp")


def test_client_creation_reports_all_missing_configuration(monkeypatch):
    for name in ("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "REDIRECT_URI"):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(RuntimeError) as error:
        spotify_fetch.create_spotify_client()

    message = str(error.value)
    assert "SPOTIFY_CLIENT_ID" in message
    assert "SPOTIFY_CLIENT_SECRET" in message
    assert "REDIRECT_URI" in message


def test_client_is_created_only_after_explicit_request(monkeypatch):
    oauth = Mock(name="auth_manager")
    oauth_factory = Mock(return_value=oauth)
    client = Mock(name="spotify_client")
    spotify_factory = Mock(return_value=client)
    monkeypatch.setattr(spotify_fetch, "SpotifyOAuth", oauth_factory)
    monkeypatch.setattr(spotify_fetch.spotipy, "Spotify", spotify_factory)

    result = spotify_fetch.create_spotify_client(
        client_id="client-id",
        client_secret="client-secret",
        redirect_uri="http://127.0.0.1:8080/callback",
    )

    assert result is client
    oauth_factory.assert_called_once_with(
        client_id="client-id",
        client_secret="client-secret",
        redirect_uri="http://127.0.0.1:8080/callback",
        scope=spotify_fetch.SPOTIFY_SCOPE,
    )
    spotify_factory.assert_called_once_with(auth_manager=oauth)


def test_playlist_functions_use_the_explicit_client():
    client = Mock()
    client.current_user_playlists.return_value = {
        "items": [{"name": "My Playlist", "id": "playlist-id"}]
    }
    client.playlist_tracks.return_value = {
        "items": [
            {
                "track": {
                    "name": "Track Name",
                    "artists": [{"name": "Artist Name"}],
                }
            }
        ]
    }

    playlists = spotify_fetch.get_playlists(client)
    tracks = spotify_fetch.get_tracks_from_playlist(client, "playlist-id")

    assert playlists == [
        {"original_name": "My Playlist", "sanitized_name": "My_Playlist", "id": "playlist-id"}
    ]
    assert tracks == [{"name": "Track Name", "artist": "Artist Name"}]
