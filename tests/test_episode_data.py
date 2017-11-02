from tv_series_name_expander import EpisodeData
from nose.tools import *


class TestEpisodeData():
    test_class = None

    def test_process_file_path(self):
        # GIVEN
        test = EpisodeData("")
        file_path="/mnt/tv_series/fargo/season_1/s01e02.avi"
        # WHEN
        test.process_file_path_parts(file_path)
        # THEN
        eq_(test.original_file_name, "s01e02")
        eq_(test.file_directory, "/mnt/tv_series/fargo/season_1")

    def test_normalize_episode_file_with_no_season_data_and_spaces(self):
        # GIVEN
        test = EpisodeData("")
        file_name = "[AC] Psycho-Pass - 01 [Blu-Ray][720p][Dual Audio][Lucifer22].mkv"
        # WHEN
        result = test.normalize_episode_name(file_name)
        # THEN
        eq_(result, "[AC] Psycho-Pass - 01 [Blu-Ray][720p][Dual Audio][Lucifer22].mkv")

    def test_normalize_episode_file_with_no_season_data_and_underscores(self):
        # GIVEN
        test = EpisodeData("")
        file_name = "[V-A]_hack_SIGN_-_01_[BB601406].mkv"
        # WHEN
        result = test.normalize_episode_name(file_name)
        # THEN
        eq_(result, "[V-A]_hack_SIGN_-_01_[BB601406].mkv")

    def test_normalize_episode_file_name_with_SxE(self):
        # GIVEN
        file_name = '04x09_lektor.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.normalize_episode_name(file_name)
        # THEN
        eq_(result, 'S04E09_lektor.avi')

    def test_normalize_episode_file_name_already_correct(self):
        # GIVEN
        file_name = 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.normalize_episode_name(file_name)
        # THEN
        eq_(result, 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi')

    def test_normalize_episode_file_name_double_episode(self):
        # GIVEN
        file_name = 'Luther.S03E03-04.PL.HDTV.XviD.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.normalize_episode_name(file_name)
        # THEN
        eq_(result, 'Luther.S03E03E04.PL.HDTV.XviD.avi')

    def test_normalize_episode_file_name_SE_on_end(self):
        # GIVEN
        file_name = 'Mentalista.DVBRiP.PL.S01E01.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.normalize_episode_name(file_name)
        # THEN
        eq_(result, 'Mentalista.DVBRiP.PL.S01E01.avi')

    def test_normalize_episdoe_file_name_lowercase(self):
        # GIVEN
        file_name = 'Luther.s01e01.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.normalize_episode_name(file_name)
        # THEN
        eq_(result, 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi')

    ################################################################################
    def test_add_episode_name_without_series_name(self):
        # GIVEN
        file_name = 'S04E09_lektor'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.add_episode_name(file_name, 'Scarlet Ribbons')
        # THEN
        eq_(result, 'S04E09.Scarlet Ribbons_lektor')

    def test_add_episode_name_standard_name(self):
        # GIVEN
        file_name = 'Luther.S01E01.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.add_episode_name(file_name, 'Episode 1')
        # THEN
        eq_(result, 'Luther.S01E01.Episode 1.PL.WEB-DL.XviD-DeiX.avi')

    def test_add_episode_name_to_alread_added(self):
        # GIVEN
        file_name = 'Luther.S01E01.Episode 1.PL.WEB-DL.XviD-DeiX.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        result = episode_data.add_episode_name(file_name, 'Episode 1')
        # THEN
        eq_(result, 'Luther.S01E01.Episode 1.PL.WEB-DL.XviD-DeiX.avi')

    ################################################################################
    def test_episode_data_process_file_name_1(self):
        # GIVEN
        file_name = '04x09_lektor.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        episode_data.process()
        # THEN
        eq_(episode_data.season, 4)
        eq_(episode_data.episode_start_nr, 9)

    def test_episode_data_process_file_name_2(self):
        # GIVEN
        file_name = 'Luther.S03E03-04.PL.HDTV.XviD.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        episode_data.process()
        # THEN
        eq_(episode_data.season, 3)
        eq_(episode_data.episode_start_nr, 3)
        eq_(episode_data.episode_end_nr, 4)

    def test_episode_data_process_file_name_3(self):
        # GIVEN
        file_name = 'Luther.s03e03-04.PL.HDTV.XviD.avi'
        episode_data = EpisodeData(file_name)
        # WHEN
        episode_data.process()
        # THEN
        eq_(episode_data.season, 3)
        eq_(episode_data.episode_start_nr, 3)
        eq_(episode_data.episode_end_nr, 4)

