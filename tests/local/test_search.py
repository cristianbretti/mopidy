from __future__ import unicode_literals

import unittest
from mopidy.local import search
from mopidy.models import Album, Track

import pytest 
class LocalLibrarySearchTest(unittest.TestCase):
	
	#Andreas
	def test_enhance_validate_query1(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		with self.assertRaises(LookupError):
			search.find_exact(tracks, {'hello': []})
	#Tai
	def test_enhance_validate_query2(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		with self.assertRaises(LookupError):
			search.find_exact(tracks, {'hello': ['foo',None]})
	#Tai
	def test_enhance_search1(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		with self.assertRaises(LookupError):
			search.search(tracks, {'hello': ['foo']})
	#Tai
	def test_enhance_search2(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		search_result = search.search(tracks, {'album': ['foo']},limit=None)
		self.assertEqual(search_result.tracks, tuple(expected_tracks))
	#Andreas
	def test_enhance_find_exact1(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		with self.assertRaises(LookupError):
			search.find_exact(tracks, {'hello': ['foo']})
	#Andreas
	def test_enhace_find_exact2(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks
		search_result = search.find_exact(tracks, {'album': ['foo']},limit=None)
		self.assertEqual(search_result.tracks, tuple(expected_tracks))
		
	def test_find_exact_with_album_query(self):
		expected_tracks = [Track(album=Album(name='foo'))]
		tracks = [Track(), Track(album=Album(name='bar'))] + expected_tracks

		search_result = search.find_exact(tracks, {'album': ['foo']})
		self.assertEqual(search_result.tracks, tuple(expected_tracks))
