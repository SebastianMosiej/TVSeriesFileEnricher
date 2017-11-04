import os
from nose.tools import *
from mock import mock_open, patch, MagicMock, Mock

try:
    from tv_series_name_expander import TVSeriesFileEnchancer, EpisodeData, files_extension
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from tv_series_name_expander import TVSeriesFileEnchancer, EpisodeData, files_extension


test_directory = "test_directory"

class TestDirkGentlys():
    episode_txt_content ='1       "Horizons"\n' \
                         '2       "Lost & Found"\n' \
                         '3       "Rogue Wall Enthusiasts"\n' \
                         '4       "Watkin"\n' \
                         '5       "Very Erectus"\n' \
                         '6       "Fix Everything"\n' \
                         '7       "Weaponized Soul"\n' \
                         '8       "Two Sane Guys Doing Normal Things"\n'
    test_files_list = [ 'S01.1080p.BluRay.x264-SHORTBREHD.nfo',
                    'S01E01.1080p.BluRay.x264-SHORTBREHD.mkv',
                    'S01E02.1080p.BluRay.x264-SHORTBREHD.mkv',
                    'S01E03.1080p.BluRay.x264-SHORTBREHD.mkv',
                    'S01E04.1080p.BluRay.x264-SHORTBREHD.mkv',
                    'S01E05.1080p.BluRay.x264-SHORTBREHD.mkv',
                    'S01E06.1080p.BluRay.x264-SHORTBREHD.mkv',
                    'S01E07.1080p.BluRay.x264-SHORTBREHD.mkv',
                    'S01E08.1080p.BluRay.x264-SHORTBREHD.mkv']

    result_files_list = [ 'S01.1080p.BluRay.x264-SHORTBREHD.nfo',
                     'S01E01.Horizons.1080p.BluRay.x264-SHORTBREHD.mkv',
                     'S01E02.Lost.&.Found.1080p.BluRay.x264-SHORTBREHD.mkv',
                     'S01E03.Rogue.Wall.Enthusiasts.1080p.BluRay.x264-SHORTBREHD.mkv',
                     'S01E04.Watkin.1080p.BluRay.x264-SHORTBREHD.mkv',
                     'S01E05.Very.Erectus.1080p.BluRay.x264-SHORTBREHD.mkv',
                     'S01E06.Fix.Everything.1080p.BluRay.x264-SHORTBREHD.mkv',
                     'S01E07.Weaponized.Soul.1080p.BluRay.x264-SHORTBREHD.mkv',
                     'S01E08.Two.Sane.Guys.Doing.Normal.Things.1080p.BluRay.x264-SHORTBREHD.mkv']

    @staticmethod
    def clean_folder_content(folder_path):
        if not os.path.exists(folder_path):
            return
        listedDir = os.listdir(folder_path)
        for file_name in listedDir:
            name, file_ext = os.path.splitext(file_name)
            if file_ext in files_extension:
                ofile = os.path.join(folder_path, file_name)
                os.remove(ofile)

    @staticmethod
    def create_sutfiles(folder_path, files_list):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            return
        for file_name in files_list:
            ofile = os.path.join(folder_path, file_name)
            open(ofile, 'a').close()

    def setUp(self):
        TestDirkGentlys.clean_folder_content(test_directory)
        TestDirkGentlys.create_sutfiles(test_directory, self.test_files_list)

    def test_add_episodes_names(self):
        # GIVEN
        m = mock_open(read_data=self.episode_txt_content)
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        with patch('tv_series_name_expander.open', m, create=True):
            sut = TVSeriesFileEnchancer()
            # WHEN
            sut.process([test_directory])
            # THEN
            m.assert_called_once_with(os.path.join(test_directory,"episodes.txt"), "r")
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[0])))
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[1])))
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[2])))
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[3])))
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[4])))
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[5])))
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[6])))
            ok_(os.path.exists(os.path.join(test_directory, self.result_files_list[7])))
