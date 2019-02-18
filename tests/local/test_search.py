from __future__ import unicode_literals

import unittest
from mopidy.local import search
from mopidy.models import Album, Track

import pytest 
class LocalLibrarySearchTest(unittest.TestCase):
	

	def test_enhance_validate_query(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		with self.assertRaises(LookupError):
			search.find_exact(tracks, {'hello': []})
		with self.assertRaises(LookupError):
			search.find_exact(tracks, {'hello': ['foo',None]})

	def test_enhace_search(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		with self.assertRaises(LookupError):
			search.search(tracks, {'hello': ['foo']})
		search_result = search.search(tracks, {'album': ['foo']},limit=None)
		self.assertEqual(search_result.tracks, tuple(expected_tracks))

	def test_enhance_find_exact(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		with self.assertRaises(LookupError):
			search.find_exact(tracks, {'hello': ['foo']})
		search_result = search.find_exact(tracks, {'album': ['foo']},limit=None)
		self.assertEqual(search_result.tracks, tuple(expected_tracks))
		
	def test_find_exact_with_album_query(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks

		search_result = search.find_exact(tracks, {'album': ['foo']})
		self.assertEqual(search_result.tracks, tuple(expected_tracks))
