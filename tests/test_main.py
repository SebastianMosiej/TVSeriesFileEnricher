import os.path
from os import listdir, getcwd
from nose.tools import *
from mock import mock_open, patch, MagicMock, Mock, call

try:
    from tv_series_name_expander import TVSeriesFileEnchancer, EpisodeData, files_extension
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from tv_series_name_expander import TVSeriesFileEnchancer, EpisodeData, files_extension


test_directory = "test_directory"
episode_txt_content ='1\t"Scarlet Ribbons"\n'\
                     '2\t"Little Red Book"\n'\
                     '3\t"Pretty Red Balloon"\n'\
                     '4\t"Ring Around the Rosie"\n'\
                     '5\t"Blood and Sand"\n'\
                     '6\t"Where in the World Is Carmine O\'Brien"\n'\
                     '7\t"Blinking Red Light"\n'\
                     '8\t"Pink Tops"\n'\
                     '9\t"The Redshirt"\n'\
                     '10\t"Fugue in Red"\n'\
                     '11\t"Always Bet on Red"\n'\
                     '12\t"My Bloody Valentine"\n'\
                     '13\t"Red is the New Black"\n'\
                     '14\t"At First Blush"\n'\
                     '15\t"War of the Roses"\n'\
                     '16\t"His Thoughts Were Red Thoughts"\n' \
                     '17\t"Cheap Burgundy"\n'\
                     '18\t"Ruddy Cheeks"\n'\
                     '19\t"Pink Champagne on Ice"\n'\
                     '20\t"Something\'s Rotten in Redmund"\n'\
                     '21\t"Ruby Slippers"\n'\
                     '22\t"So Long, and Thanks for All the Red Snapper"\n'\
                     '23\t"Red Rover, Red Rover"\n'\
                     '24\t"The Crimson Hat"\n'
test_files_list = [
    '04x01_lektor.avi',
    '04x02_lektor.avi',
    '04x03_lektor.avi',
    '04x04_lektor.avi',
    '04x05_lektor.avi',
    '04x06_lektor.avi',
    '04x07_lektor.avi',
    '04x08_lektor.avi',
    '04x09_lektor.avi',
    '04x10_lektor.avi',
    '04x11_lektor.avi',
    '04x12_lektor.avi',
    '04x13_lektor.avi',
    '04x14_lektor.avi',
    '04x15_lektor.avi',
    '04x16_lektor.avi',
    '04x17_lektor.avi',
    '04x18_lektor.avi',
    '04x19_lektor.avi',
    '04x20_lektor.avi',
    '04x21_lektor.avi',
    '04x22_lektor.avi',
    '04x23_lektor.avi',
    '04x24_lektor.avi']


def clean_folder_content(folder_path):
    if not os.path.exists(folder_path):
        return
    listedDir = os.listdir(folder_path)
    for file_name in listedDir:
        name, file_ext = os.path.splitext(file_name)
        if file_ext in files_extension:
            ofile = os.path.join(folder_path, file_name)
            os.remove(ofile)


def create_sutfiles(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        return
    for file_name in test_files_list:
        ofile = os.path.join(folder_path, file_name)
        open(ofile, 'a').close()


class TestTVSeriesFileEnchancer():
    test_class = None

    def setUp(self):
        clean_folder_content(os.path.join(os.getcwd(), test_directory))
        create_sutfiles(os.path.join(os.getcwd(), test_directory))
        self.test_class = TVSeriesFileEnchancer()

    def tearDown(self):
        del self.test_class

    ################################################################################
    def test_get_files_list(self):
        # GIVEN / WHEN
        self.test_class.gather_files_list([test_directory])
        # THEN
        eq_(len(self.test_class.episodes_list), 24)
        eq_(self.test_class.episodes_list[0].file_name, 'S04E01_lektor')
        eq_(self.test_class.episodes_list[1].file_name, 'S04E02_lektor')
        eq_(self.test_class.episodes_list[23].file_name, 'S04E24_lektor')

    ################################################################################
    def test_load_episodes_names_file(self):
        # GIVEN
        m = mock_open(read_data=episode_txt_content)
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        with patch('tv_series_name_expander.open', m, create=True):
            # WHEN
            self.test_class.load_episode_names(test_directory)
            # THEN
            eq_(len(self.test_class.episodes_names), 24)
            eq_(self.test_class.episodes_names[1], 'Scarlet Ribbons')
            eq_(self.test_class.episodes_names[2], 'Little Red Book')
            eq_(self.test_class.episodes_names[3], 'Pretty Red Balloon')

    ################################################################################
    @patch('tv_series_name_expander.os.path.isdir', return_value=True)
    @patch("tv_series_name_expander.os.listdir", return_value=test_files_list)
    @patch("tv_series_name_expander.os.rename")
    def test_enrich_episodes_1(self, RenameFileMock, ListDirMock, IsDirMock):
        # GIVEN
        m = mock_open(read_data=episode_txt_content)
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        with patch('tv_series_name_expander.open', m, create=True):
            # WHEN
            self.test_class.process([test_directory])
            # THEN
            m.assert_called_once_with(os.path.join(test_directory,"episodes.txt"), "r")
            isDirMockCalls = IsDirMock.mock_calls

            eq_(isDirMockCalls[0], call(os.path.join(os.getcwd(),test_directory)))
            eq_(isDirMockCalls[1], call(test_directory))

            abs_test_dir = os.path.join(os.getcwd(), test_directory)
            renameFilesCalls = RenameFileMock.mock_calls
            eq_(renameFilesCalls[0], call(os.path.join(abs_test_dir, '04x01_lektor.avi'), os.path.join(abs_test_dir, "S04E01.Scarlet.Ribbons_lektor.avi")))
            eq_(renameFilesCalls[1], call(os.path.join(abs_test_dir, '04x02_lektor.avi'), os.path.join(abs_test_dir, "S04E02.Little.Red.Book_lektor.avi")))
            eq_(renameFilesCalls[2], call(os.path.join(abs_test_dir, '04x03_lektor.avi'), os.path.join(abs_test_dir, "S04E03.Pretty.Red.Balloon_lektor.avi")))
            eq_(renameFilesCalls[23], call(os.path.join(abs_test_dir, '04x24_lektor.avi'), os.path.join(abs_test_dir, "S04E24.The.Crimson.Hat_lektor.avi")))

