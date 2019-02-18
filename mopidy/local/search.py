from __future__ import absolute_import, unicode_literals

from mopidy.models import SearchResult

Search_Cov = [False]*18
FindExact_Cov = [False]*18
def find_exact(tracks, query=None, limit=100, offset=0, uris=None):
    """
    Filter a list of tracks where ``field`` is ``values``.

    :param list tracks: a list of :class:`~mopidy.models.Track`
    :param dict query: one or more field/value pairs to search for
    :param int limit: maximum number of results to return
    :param int offset: offset into result set to use.
    :param uris: zero or more URI roots to limit the search to
    :type uris: list of strings or :class:`None`
    :rtype: :class:`~mopidy.models.SearchResult`
    """
    # TODO Only return results within URI roots given by ``uris``
    FindExact_Cov[0] = True
    if query is None:
	FindExact_Cov[1] = True
        query = {}

    _validate_query(query)

    for (field, values) in query.items():
        # FIXME this is bound to be slow for large libraries
	FindExact_Cov[2] = True
        for value in values:
    	    FindExact_Cov[3] = True
            if field == 'track_no':
                q = _convert_to_int(value)
            else:
		FindExact_Cov[4] = True
                q = value.strip()

            def uri_filter(t):
                return q == t.uri

            def track_name_filter(t):
                return q == t.name

            def album_filter(t):
                return q == getattr(getattr(t, 'album', None), 'name', None)

            def artist_filter(t):
                return filter(lambda a: q == a.name, t.artists)

            def albumartist_filter(t):
                return any([
                    q == a.name for a in getattr(t.album, 'artists', [])])

            def composer_filter(t):
                return any([q == a.name for a in getattr(t, 'composers', [])])

            def performer_filter(t):
                return any([q == a.name for a in getattr(t, 'performers', [])])

            def track_no_filter(t):
                return q == t.track_no

            def genre_filter(t):
                return (t.genre and q == t.genre)

            def date_filter(t):
                return q == t.date

            def comment_filter(t):
                return q == t.comment

            def any_filter(t):
                return (uri_filter(t) or
                        track_name_filter(t) or
                        album_filter(t) or
                        artist_filter(t) or
                        albumartist_filter(t) or
                        composer_filter(t) or
                        performer_filter(t) or
                        track_no_filter(t) or
                        genre_filter(t) or
                        date_filter(t) or
                        comment_filter(t))

            if field == 'uri':
                tracks = filter(uri_filter, tracks)
            elif field == 'track_name':
                FindExact_Cov[5] = True;
                tracks = filter(track_name_filter, tracks)
            elif field == 'album':
                FindExact_Cov[6] = True;
                tracks = filter(album_filter, tracks)
            elif field == 'artist':
                FindExact_Cov[7] = True;
                tracks = filter(artist_filter, tracks)
            elif field == 'albumartist':
                FindExact_Cov[8] = True;
                tracks = filter(albumartist_filter, tracks)
            elif field == 'composer':
                FindExact_Cov[9] = True;
                tracks = filter(composer_filter, tracks)
            elif field == 'performer':
                FindExact_Cov[10] = True;
                tracks = filter(performer_filter, tracks)
            elif field == 'track_no':
                FindExact_Cov[11] = True;
                tracks = filter(track_no_filter, tracks)
            elif field == 'genre':
                FindExact_Cov[12] = True;
                tracks = filter(genre_filter, tracks)
            elif field == 'date':
                FindExact_Cov[13] = True;
                tracks = filter(date_filter, tracks)
            elif field == 'comment':
                FindExact_Cov[14] = True;
                tracks = filter(comment_filter, tracks)
            elif field == 'any':
                FindExact_Cov[15] = True;
                tracks = filter(any_filter, tracks)
            else:
                FindExact_Cov[16] = True;
                raise LookupError('Invalid lookup field: %s' % field)

    if limit is None:
        tracks = tracks[offset:]
    else:
        FindExact_Cov[17] = True;
        tracks = tracks[offset:offset + limit]
    # TODO: add local:search:<query>
    return SearchResult(uri='local:search', tracks=tracks)


def search(tracks, query=None, limit=100, offset=0, uris=None):
    """
    Filter a list of tracks where ``field`` is like ``values``.

    :param list tracks: a list of :class:`~mopidy.models.Track`
    :param dict query: one or more field/value pairs to search for
    :param int limit: maximum number of results to return
    :param int offset: offset into result set to use.
    :param uris: zero or more URI roots to limit the search to
    :type uris: list of strings or :class:`None`
    :rtype: :class:`~mopidy.models.SearchResult`
    """
    # TODO Only return results within URI roots given by ``uris``
    Search_Cov[0] = True
    if query is None:
        Search_Cov[1] = True
        query = {}

    _validate_query(query)

    for (field, values) in query.items():
        # FIXME this is bound to be slow for large libraries
        Search_Cov[2] = True
        for value in values:
            Search_Cov[3] = True
            if field == 'track_no':
                q = _convert_to_int(value)
            else:
                Search_Cov[4] = True
                q = value.strip().lower()

            def uri_filter(t):
                return bool(t.uri and q in t.uri.lower())

            def track_name_filter(t):
                return bool(t.name and q in t.name.lower())

            def album_filter(t):
                return bool(t.album and t.album.name and
                            q in t.album.name.lower())

            def artist_filter(t):
                return bool(filter(
                    lambda a: bool(a.name and q in a.name.lower()), t.artists))

            def albumartist_filter(t):
                return any([a.name and q in a.name.lower()
                            for a in getattr(t.album, 'artists', [])])

            def composer_filter(t):
                return any([a.name and q in a.name.lower()
                            for a in getattr(t, 'composers', [])])

            def performer_filter(t):
                return any([a.name and q in a.name.lower()
                            for a in getattr(t, 'performers', [])])

            def track_no_filter(t):
                return q == t.track_no

            def genre_filter(t):
                return bool(t.genre and q in t.genre.lower())

            def date_filter(t):
                return bool(t.date and t.date.startswith(q))

            def comment_filter(t):
                return bool(t.comment and q in t.comment.lower())

            def any_filter(t):
                return (uri_filter(t) or
                        track_name_filter(t) or
                        album_filter(t) or
                        artist_filter(t) or
                        albumartist_filter(t) or
                        composer_filter(t) or
                        performer_filter(t) or
                        track_no_filter(t) or
                        genre_filter(t) or
                        date_filter(t) or
                        comment_filter(t))

            if field == 'uri':
                Search_Cov[5] = True
                tracks = filter(uri_filter, tracks)
            elif field == 'track_name':
                Search_Cov[6] = True
                tracks = filter(track_name_filter, tracks)
            elif field == 'album':
                Search_Cov[7] = True
                tracks = filter(album_filter, tracks)
            elif field == 'artist':
                Search_Cov[8] = True
                tracks = filter(artist_filter, tracks)
            elif field == 'albumartist':
                Search_Cov[9] = True
                tracks = filter(albumartist_filter, tracks)
            elif field == 'composer':
                Search_Cov[10] = True
                tracks = filter(composer_filter, tracks)
            elif field == 'performer':
                Search_Cov[11] = True
                tracks = filter(performer_filter, tracks)
            elif field == 'track_no':
                Search_Cov[12] = True
                tracks = filter(track_no_filter, tracks)
            elif field == 'genre':
                Search_Cov[13] = True
                tracks = filter(genre_filter, tracks)
            elif field == 'date':
                Search_Cov[14] = True
                tracks = filter(date_filter, tracks)
            elif field == 'comment':
                Search_Cov[15] = True
                tracks = filter(comment_filter, tracks)
            elif field == 'any':
                Search_Cov[16] = True
                tracks = filter(any_filter, tracks)
            else:
                raise LookupError('Invalid lookup field: %s' % field)

    if limit is None:
        tracks = tracks[offset:]
    else:
        Search_Cov[17] = True
        tracks = tracks[offset:offset + limit]
    # TODO: add local:search:<query>
    return SearchResult(uri='local:search', tracks=tracks)


def _validate_query(query):
    for (_, values) in query.items():
        if not values:
            raise LookupError('Missing query')
        for value in values:
            if not value:
                raise LookupError('Missing query')


def _convert_to_int(string):
    try:
        return int(string)
    except ValueError:
        return object()
