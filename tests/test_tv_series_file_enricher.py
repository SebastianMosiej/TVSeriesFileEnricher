import unittest
import os
from TVSeriesFileEnricher import TVSeriesFileEnchancer, EpisodeData, files_extension

# try:
#     import HTTPConnector
# except ImportError:    
#     sys.path.append(os.path.join(os.path.dirname(__file__),".."))
#     sys.path.append(os.path.dirname(__file__))
# import HTTPConnector

test_directory = "test_directory"
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
    listedDir = os.listdir(folder_path)
    for file_name in listedDir:
        name, file_ext = os.path.splitext(file_name)
        if file_ext in files_extension:
            ofile = os.path.join(folder_path, file_name)
            os.remove(ofile)


def create_test_files(folder_path):
    for file_name in test_files_list:
        ofile = os.path.join(folder_path, file_name)
        open(ofile, 'a').close()


class TVSeriesFileEnchancerTest(unittest.TestCase):
    test_class = None

    def setUp(self):
        clean_folder_content(os.path.join(os.getcwd(), test_directory))
        create_test_files(os.path.join(os.getcwd(), test_directory))
        self.test_class = TVSeriesFileEnchancer()

    def tearDown(self):
        del self.test_class

    ################################################################################

    def test_rename_episodeid_to_full_name_1(self):
        file_name = '04x09_lektor.avi'
        episode_data = EpisodeData(file_name)
        result = episode_data.rename_episodeid_to_full(file_name)
        self.assertEqual(result, 'S04E09_lektor.avi')

    def test_rename_episodeid_to_full_name_2(self):
        file_name = 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        result = episode_data.rename_episodeid_to_full(file_name)
        self.assertEqual(result, 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi')

    def test_rename_episodeid_to_full_name_3(self):
        file_name = 'Luther.S03E03-04.PL.HDTV.XviD.avi'
        episode_data = EpisodeData(file_name)
        result = episode_data.rename_episodeid_to_full(file_name)
        self.assertEqual(result, 'Luther.S03E03E04.PL.HDTV.XviD.avi')

    def test_rename_episodeid_to_full_name_4(self):
        file_name = 'Mentalista.DVBRiP.PL.S01E01.avi'
        episode_data = EpisodeData(file_name)
        result = episode_data.rename_episodeid_to_full(file_name)
        self.assertEqual(result, 'Mentalista.DVBRiP.PL.S01E01.avi')

    def test_rename_episodeid_to_full_name_5(self):
        file_name = 'Luther.s01e01.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        result = episode_data.rename_episodeid_to_full(file_name)
        self.assertEqual(result, 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi')

    ################################################################################
    def test_episode_data_process_file_name_1(self):
        file_name = '04x09_lektor.avi'
        episode_data = EpisodeData(file_name)
        self.assertEqual(episode_data.season, 4)
        self.assertEqual(episode_data.episode_start_nr, 9)

    def test_episode_data_process_file_name_2(self):
        file_name = 'Luther.S03E03-04.PL.HDTV.XviD.avi'
        episode_data = EpisodeData(file_name)
        self.assertEqual(episode_data.season, 3)
        self.assertEqual(episode_data.episode_start_nr, 3)
        self.assertEqual(episode_data.episode_end_nr, 4)

    def test_episode_data_process_file_name_3(self):
        file_name = 'Luther.s03e03-04.PL.HDTV.XviD.avi'
        episode_data = EpisodeData(file_name)
        self.assertEqual(episode_data.season, 3)
        self.assertEqual(episode_data.episode_start_nr, 3)
        self.assertEqual(episode_data.episode_end_nr, 4)

    ################################################################################
    def test_get_files_list(self):
        #         self.test_class.getFilesList([os.getcwd()+os.sep+test_directory])
        self.test_class._TVSeriesFileEnchancer__get_files_list([test_directory])
        self.assertEqual(len(self.test_class.episodes_list), 24)
        self.assertEqual(self.test_class.episodes_list[0].file_name, 'S04E01_lektor')
        self.assertEqual(self.test_class.episodes_list[1].file_name, 'S04E02_lektor')
        self.assertEqual(self.test_class.episodes_list[23].file_name, 'S04E24_lektor')

    ################################################################################
    def test_add_episode_name_1(self):
        file_name = 'S04E09_lektor'
        episode_data = EpisodeData(file_name)
        result = episode_data.add_episode_name(file_name, 'Scarlet Ribbons')
        self.assertEqual(result, 'S04E09.Scarlet Ribbons_lektor')

    def test_add_episode_name_2(self):
        file_name = 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        result = episode_data.add_episode_name(file_name, 'Episode 1')
        self.assertEqual(result, 'Luther.S01E01.Episode 1.PL.WEB-DL.XviD-DeiX.avi')

    def test_add_episode_name_3(self):
        file_name = 'Luther.S01E01.Episode 1.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        result = episode_data.add_episode_name(file_name, 'Episode 1')
        self.assertEqual(result, 'Luther.S01E01.Episode 1.PL.WEB-DL.XviD-DeiX.avi')

    ################################################################################
    def test_load_episodes_names_file(self):
        self.test_class._TVSeriesFileEnchancer__load_file_with_episode_names(test_directory)
        self.assertEqual(len(self.test_class.episodes_names), 24)
        self.assertEqual(self.test_class.episodes_names[1], 'Scarlet Ribbons')
        self.assertEqual(self.test_class.episodes_names[2], 'Little Red Book')

    ################################################################################
    def test_enrich_episodes_1(self):
        self.test_class.run([test_directory])
        abs_test_dir = os.path.join(os.getcwd(), test_directory)
        self.assertTrue(os.path.exists(os.path.join(abs_test_dir, "S04E01.Scarlet Ribbons_lektor.avi")))
        self.assertTrue(os.path.exists(os.path.join(abs_test_dir, "S04E02.Little Red Book_lektor.avi")))
        self.assertTrue(os.path.exists(os.path.join(abs_test_dir, "S04E03.Pretty Red Balloon_lektor.avi")))
        self.assertTrue(os.path.exists(os.path.join(abs_test_dir, "S04E04.Ring Around the Rosie_lektor.avi")))
        self.assertTrue(os.path.exists(os.path.join(abs_test_dir, "S04E05.Blood and Sand_lektor.avi")))
