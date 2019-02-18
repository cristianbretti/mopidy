from __future__ import absolute_import, unicode_literals

import datetime
import logging
import re

from mopidy.models import TlTrack
from mopidy.mpd.protocol import tagtype_list


logger = logging.getLogger(__name__)

# TODO: special handling of local:// uri scheme
normalize_path_re = re.compile(r'[^/]+')


def normalize_path(path, relative=False):
    parts = normalize_path_re.findall(path or '')
    if not relative:
        parts.insert(0, '')
    return '/'.join(parts)


def get_stream_title(stream_title, track):
    if stream_title is not None:
        return ('Title', stream_title)
    else:
        return ('Title', track.name or '')


def get_track_name(stream_title, track):
    if stream_title is not None and track.name:
        return ('Name', track.name)


def get_track_date(track):
    if track.date:
        return ('Date', track.date)


def get_track_value(track):
    if track.album is not None and track.album.num_tracks is not None:
        return ('Track', '%d/%d' % (
            track.track_no or 0, track.album.num_tracks))
    else:
        return ('Track', track.track_no or 0)


def get_pos(position, tlid):
    if position is not None and tlid is not None:
        return ('Pos', position)


def get_id(position, tlid):
    if position is not None and tlid is not None:
        return ('Id', tlid)


def get_musicbrainz_albumid(track):
    if track.album is not None and track.album.musicbrainz_id is not None:
        return ('MUSICBRAINZ_ALBUMID', track.album.musicbrainz_id)


def get_albumartists(track):
    if track.album is not None and track.album.artists:
        return ('AlbumArtist', concat_multi_values(track.album.artists, 'name'))


def get_musicbrainz_albumartistid(track):
    if track.album is not None and track.album.artists:
        musicbrainz_ids = concat_multi_values(
            track.album.artists, 'musicbrainz_id')
        if musicbrainz_ids:
            return ('MUSICBRAINZ_ALBUMARTISTID', musicbrainz_ids)


def get_track_artist(track):
    if track.artists:
        musicbrainz_ids = concat_multi_values(track.artists, 'musicbrainz_id')
        if musicbrainz_ids:
            return ('MUSICBRAINZ_ARTISTID', musicbrainz_ids)


def get_track_composers(track):
    if track.composers:
        return ('Composer', concat_multi_values(track.composers, 'name'))


def get_track_performers(track):
    if track.performers:
        return ('Performer', concat_multi_values(track.performers, 'name'))


def get_track_genre(track):
    if track.genre:
        return ('Genre', track.genre)


def get_disc_no(track):
    if track.disc_no:
        return ('Disc', track.disc_no)


def get_last_modified(track):
    if track.last_modified:
        datestring = datetime.datetime.utcfromtimestamp(
            track.last_modified // 1000).isoformat()
        return ('Last-Modified', datestring + 'Z')


def get_musicbrainz_id(track):
    if track.musicbrainz_id is not None:
        return ('MUSICBRAINZ_TRACKID', track.musicbrainz_id)


def get_album_uri(track):
    if track.album and track.album.uri:
        return ('X-AlbumUri', track.album.uri)


def get_album_images(track):
    if track.album and track.album.images:
        images = ';'.join(i for i in track.album.images if i != '')
        return ('X-AlbumImage', images)


def track_to_mpd_format(track, position=None, stream_title=None):
    """
    Format track for output to MPD client.

    :param track: the track
    :type track: :class:`mopidy.models.Track` or :class:`mopidy.models.TlTrack`
    :param position: track's position in playlist
    :type position: integer
    :param stream_title: the current streams title
    :type position: string
    :rtype: list of two-tuples
    """
    if isinstance(track, TlTrack):
        (tlid, track) = track
    else:
        (tlid, track) = (None, track)

    if not track.uri:
        logger.warning('Ignoring track without uri')
        return []

    result = [
        ('file', track.uri),
        ('Time', track.length and (track.length // 1000) or 0),
        ('Artist', concat_multi_values(track.artists, 'name')),
        ('Album', track.album and track.album.name or ''),
        get_stream_title(stream_title, track),
        get_track_name(stream_title, track),
        get_track_date(track),
        get_track_value(track),
        get_pos(position, tlid),
        get_id(position, tlid),
        get_musicbrainz_albumid(track),
        get_albumartists(track),
        get_musicbrainz_albumartistid(track),
        get_track_artist(track),
        get_track_composers(track),
        get_track_performers(track),
        get_track_genre(track),
        get_disc_no(track),
        get_last_modified(track),
        get_musicbrainz_id(track),
        get_album_uri(track),
        get_album_images(track)
    ]

    result = [
        element for element in result if element is not None and _has_value(*element)]

    return result


def _has_value(tagtype, value):
    """
    Determine whether to add the tagtype to the output or not.

    :param tagtype: the MPD tagtype
    :type tagtype: string
    :param value: the tag value
    :rtype: bool
    """
    if tagtype in tagtype_list.TAGTYPE_LIST:
        return bool(value)
    return True


def concat_multi_values(models, attribute):
    """
    Format Mopidy model values for output to MPD client.

    :param models: the models
    :type models: array of :class:`mopidy.models.Artist`,
        :class:`mopidy.models.Album` or :class:`mopidy.models.Track`
    :param attribute: the attribute to use
    :type attribute: string
    :rtype: string
    """
    # Don't sort the values. MPD doesn't appear to (or if it does it's not
    # strict alphabetical). If we just use them in the order in which they come
    # in then the musicbrainz ids have a higher chance of staying in sync
    return ';'.join(
        getattr(m, attribute)
        for m in models if getattr(m, attribute, None) is not None
    )


def tracks_to_mpd_format(tracks, start=0, end=None):
    """
    Format list of tracks for output to MPD client.

    Optionally limit output to the slice ``[start:end]`` of the list.

    :param tracks: the tracks
    :type tracks: list of :class:`mopidy.models.Track` or
        :class:`mopidy.models.TlTrack`
    :param start: position of first track to include in output
    :type start: int (positive or negative)
    :param end: position after last track to include in output
    :type end: int (positive or negative) or :class:`None` for end of list
    :rtype: list of lists of two-tuples
    """
    if end is None:
        end = len(tracks)
    tracks = tracks[start:end]
    positions = range(start, end)
    assert len(tracks) == len(positions)
    result = []
    for track, position in zip(tracks, positions):
        formatted_track = track_to_mpd_format(track, position)
        if formatted_track:
            result.append(formatted_track)
    return result


def playlist_to_mpd_format(playlist, *args, **kwargs):
    """
    Format playlist for output to MPD client.

    Arguments as for :func:`tracks_to_mpd_format`, except the first one.
    """
    return tracks_to_mpd_format(playlist.tracks, *args, **kwargs)
