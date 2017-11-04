import os.path
from os.path import join as join
from nose.tools import *
from mock import mock_open, patch, call

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

    @patch('tv_series_name_expander.os.path.isdir', return_value=True)
    @patch("tv_series_name_expander.os.listdir", return_value=test_files_list)
    @patch("tv_series_name_expander.os.rename")
    def test_add_episodes_names(self, rename_file_mock, list_dir_mock, is_dir_mock):
        # GIVEN
        m = mock_open(read_data=self.episode_txt_content)
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        with patch('tv_series_name_expander.open', m, create=True):
            sut = TVSeriesFileEnchancer()
            # WHEN
            sut.process([test_directory])
            # THEN
            m.assert_called_once_with(os.path.join(test_directory,"episodes.txt"), "r")

            is_dir_mock_calls = is_dir_mock.mock_calls
            eq_(is_dir_mock_calls[0], call(os.path.join(os.getcwd(),test_directory)))
            eq_(is_dir_mock_calls[1], call(test_directory))

            abs_test_dir = os.path.join(os.getcwd(), test_directory)
            rename_files_calls = rename_file_mock.mock_calls
            eq_(len(rename_files_calls), 8)
            eq_(rename_files_calls[0], call(join(abs_test_dir, self.test_files_list[1]), join(abs_test_dir, self.result_files_list[1])))
            eq_(rename_files_calls[1], call(join(abs_test_dir, self.test_files_list[2]), join(abs_test_dir, self.result_files_list[2])))
            eq_(rename_files_calls[2], call(join(abs_test_dir, self.test_files_list[3]), join(abs_test_dir, self.result_files_list[3])))
            eq_(rename_files_calls[3], call(join(abs_test_dir, self.test_files_list[4]), join(abs_test_dir, self.result_files_list[4])))
            eq_(rename_files_calls[4], call(join(abs_test_dir, self.test_files_list[5]), join(abs_test_dir, self.result_files_list[5])))
            eq_(rename_files_calls[5], call(join(abs_test_dir, self.test_files_list[6]), join(abs_test_dir, self.result_files_list[6])))
            eq_(rename_files_calls[6], call(join(abs_test_dir, self.test_files_list[7]), join(abs_test_dir, self.result_files_list[7])))
            eq_(rename_files_calls[7], call(join(abs_test_dir, self.test_files_list[8]), join(abs_test_dir, self.result_files_list[8])))
