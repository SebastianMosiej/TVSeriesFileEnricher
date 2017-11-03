#!/usr/bin/python2
from optparse import OptionParser
import os, re, sys
from string import maketrans

files_extension = [".avi", ".mp4", ".mkv"]
dest_episodes_file_name = "episodes.txt"

season_re_pattern = '[Ss]?\d{1,2}'
episode_re_pattern = '([-xEe]?\d{1,2}){1,2}'
episodeid_re_pattern = season_re_pattern + episode_re_pattern

""" class with data about single file """


class EpisodeData:
    episode_nr_regexp = re.compile(episode_re_pattern)
    season_nr_regexp = re.compile(season_re_pattern)
    episodeid_regexp = re.compile(episodeid_re_pattern)
    initial_path = ""

    """The constructor. """
    original_file_name = ''
    file_name = ''
    file_ext = ''
    file_directory = ''
    season = 0
    """start episode number covered by this file"""
    episode_start_nr = 0
    """end episode number - if this file contain multiple episodes"""
    episode_end_nr = 0
    episode_name = ''
    dst_files_name = ''

    def __init__(self, file_path):
        self.initial_path = file_path

    def process(self):
        self.process_file_path_parts(self.initial_path)
        self.file_name = self.normalize_episode_name(self.original_file_name)
        self.process_file_name()

    def process_file_path_parts(self, file_path):
        self.file_directory = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        self.original_file_name, self.file_ext = os.path.splitext(file_name)

    def process_file_name(self):
        episodeid_name = self.episodeid_regexp.search(self.file_name).group()
        result = self.season_nr_regexp.search(episodeid_name)
        self.season = int(result.group().translate(None, 'Ss'))

        episode_id = self.episode_nr_regexp.search(episodeid_name, result.end()).group()
        while len(episode_id):
            result = re.compile('[-xEe]?\d{1,2}').search(episode_id)
            if self.episode_start_nr == 0:
                self.episode_start_nr = int(result.group().translate(None, 'Ee'))
            episode_id = episode_id.replace(result.group(), '')
            if len(episode_id) == 0:
                self.episode_end_nr = int(result.group().translate(None, 'Ee'))

    def normalize_episode_name(self, file_name):
        episodeid_result = self.episodeid_regexp.search(file_name)
        trans = maketrans("x-es","EEES")
        name = episodeid_result.group().translate(trans)
        # name = name.replace('s', 'S')
        index = name.find('S')
        if name.find('S') < 0:
            if len(name)>2:
                name = 'S' + name
        name = file_name[:episodeid_result.start(0)]+name+file_name[episodeid_result.end(0):]
        return name

    def add_episode_name(self, file_name, episode_name):
        try:
            file_name.index(episode_name)
        except ValueError:
            episodeid_result = self.episodeid_regexp.search(file_name)
            file_name = file_name[0:episodeid_result.end()] + '.' + episode_name + file_name[episodeid_result.end():]
        return file_name

    def rename_file(self, episode_name):
        episode_name = episode_name.replace(' ','.')
        name = self.add_episode_name(self.file_name, episode_name)
        new_file_path = os.path.join(self.file_directory,name + self.file_ext)
        os.rename(self.initial_path, new_file_path)


class TVSeriesFileEnchancer:
    """The constructor.
    """
    episodes_list = []
    episodes_names = {}

    def __init__(self):
        self.episodes_list = []

    def process(self, input_file):
        #
        if not isinstance(input_file, list):
        # if not isinstance(list, input_file):
            raise AttributeError("As input use list")
        self.gather_files_list(input_file)
        self.load_episode_names(input_file[0])
        self.__rename_files()

    def __rename_files(self):
        for episode in self.episodes_list:
            episode.rename_file(self.episodes_names[episode.episode_start_nr])

    def process_line(self, line):
        split_result = line.split('"')
        return (int(split_result[0].strip()), split_result[1])

    def load_episode_names(self, input_file=""):
        if input_file == "":
            input_file = dest_episodes_file_name
        if os.path.isdir(input_file):
            input_file = input_file + "/episodes.txt"
        with open(input_file, "r") as fh:
            for line in fh:
                line = line.strip()
                if len(line) == 0: continue
                (episode_nr, episode_name) = self.process_line(line)
                self.episodes_names[episode_nr] = episode_name
        print("Episodes names loaded (", str(len(self.episodes_names)), ")")

    def gather_files_list(self, inputFilez):
        for i in inputFilez:
            abzPath = os.path.abspath(i)
            if os.path.isdir(abzPath):
                listedDir = os.listdir(abzPath)
                listedDir.sort()
                print("Looking for files in '{}'".format(abzPath))
                for f in listedDir:
                    name, file_ext = os.path.splitext(f)
                    print("Found '{}' file".format(name))
                    if file_ext in files_extension:
                        ofile = os.path.join(abzPath, f)
                        item = EpisodeData(ofile)
                        item.process()
                        self.episodes_list.append(item)
            else:
                name, file_ext = os.path.splitext(abzPath)
                if file_ext in files_extension:
                    item = EpisodeData(abzPath)
                    self.episodes_list.append(item)
        print("Found {} episodes files".format(len(self.episodes_list)))


def parse_parameters(args = None):
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="filename with list of episodes names", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    return parser.parse_args(args)


def test_required_python():
    if sys.version_info.major != 2:
        raise SystemError("Use Python2")


def clear_console():
    sys.stderr.write("\x1b[2J\x1b[H")


if __name__ == "__main__":
    test_required_python()
    clear_console()
    (options, args) = parse_parameters()
    if options.filename is None:
        options.filename = [os.getcwd()]
    test_class = TVSeriesFileEnchancer()
    test_class.process(options.filename)
