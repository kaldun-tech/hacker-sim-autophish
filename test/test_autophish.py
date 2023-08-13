import hackersim_auto_phish
import pytest
import os

SIMPLE_LIST = 'Parenting'
COMPLEX_LIST = ['Marketing', 'Documentary', 'Engineering', 'Aviation', 'Literature', 'Business', 'Manga', 'Online', 'Construction', 'Plays']

def test_phish_pngimage_terrycruz():
    cwd = os.getcwd()
    terry_cruz_fp = f'{cwd}/test/data/TerryCruz.png'
    print(f'Targeting file {terry_cruz_fp}')
    hackersim_auto_phish.phish_file(terry_cruz_fp)

def test_phish_pngimage_none():
    hackersim_auto_phish.phish_clipboard(None)

def test_find_most_likely_phish_simple():
    hackersim_auto_phish.find_most_likely_phish(SIMPLE_LIST)

def test_find_most_likely_phish_complex():
    hackersim_auto_phish.find_most_likely_phish(COMPLEX_LIST)