from optparse import OptionParser
import os, re, sys

files_extension = [".avi", ".mp4"]
dest_episodes_file_name = "episodes.txt"

""" class with data about single file """


class EpisodeData:
    """The constructor. """
    old_file_name = ''
    file_name = ''
    file_ext = ''
    file_dir = ''
    season = 0
    """start episode number covered by this file"""
    episode_start_nr = 0
    """end episode number - if this file contain multiple episodes"""
    episode_end_nr = 0
    episode_name = ''
    dst_files_name = ''

    def process_file_path_parts(self, file_path):
        self.file_dir = os.path.dirname(file_path)
        self.file_name = os.path.basename(file_path)
        self.file_name, self.file_ext = os.path.splitext(self.file_name)
        self.old_file_name = self.file_name

    def __init__(self, file_path):
        season_re_pattern = '[Ss]?\d{1,2}'
        episode_re_patern = '([-xEe]?\d{1,2}){1,2}'
        episodeid_re_pattern = season_re_pattern + episode_re_patern
        self.episode_nr_regexp = re.compile(episode_re_patern)
        self.season_nr_regexp = re.compile(season_re_pattern)
        self.episodeid_regexp = re.compile(episodeid_re_pattern)
        """The constructor."""
        self.process_file_path_parts(file_path)
        self.file_name = self.rename_episodeid_to_full(self.file_name)
        self.process_file_name()

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

    def rename_episodeid_to_full(self, file_name):
        episodeid_result = self.episodeid_regexp.search(file_name)
        old_name = episodeid_result.group()
        name = old_name.replace('x', 'E')
        name = name.replace('-', 'E')
        name = name.replace('e', 'E')
        name = name.replace('s', 'S')
        index = name.find('S')
        if index < 0: name = 'S' + name
        name = file_name.replace(old_name, name)
        return name;

    def add_episode_name(self, file_name, episode_name):
        try:
            file_name.index(episode_name);
        except ValueError:
            episodeid_result = self.episodeid_regexp.search(file_name)
            file_name = file_name[0:episodeid_result.end()] + '.' + episode_name + file_name[episodeid_result.end():]
        return file_name


class TVSeriesFileEnchancer:
    """The constructor.
    """
    episodes_list = []
    episodes_names = {}

    def __init__(self):
        self.episodes_list = []

    def run(self, input_file):
        self.__get_files_list(input_file)
        self.__load_file_with_episode_names(input_file[0])
        self.__rename_files()

    def __rename_files(self):
        for episode in self.episodes_list:
            old_file_path = episode.file_dir + os.sep + episode.old_file_name + episode.file_ext
            name = episode.add_episode_name(episode.file_name, self.episodes_names[episode.episode_start_nr])
            new_file_path = episode.file_dir + os.sep + name + episode.file_ext
            os.rename(old_file_path, new_file_path)

    def process_line(self, line):
        split_result = line.split('"')
        return (int(split_result[0].strip()), split_result[1])

    def __load_file_with_episode_names(self, input_file=""):
        if input_file == "":
            input_file = dest_episodes_file_name
        if os.path.isdir(input_file):
            input_file = input_file + "/episodes.txt"
        fh = open(input_file, "r")
        for line in fh:
            line = line.strip()
            if len(line) == 0: continue
            (episode_nr, episode_name) = self.process_line(line)
            self.episodes_names[episode_nr] = episode_name
        print("Episodes names loaded (", str(len(self.episodes_names)), ")")

    def __get_files_list(self, inputFilez):
        """The constructor."""
        for i in inputFilez:
            abzPath = os.path.abspath(i)
            if os.path.isdir(abzPath):
                listedDir = os.listdir(abzPath)
                listedDir.sort()
                print("Looking for files in '", abzPath, ",")
                for f in listedDir:
                    name, file_ext = os.path.splitext(f)
                    print("Found '", name, "' file")
                    if file_ext in files_extension:
                        ofile = os.path.join(abzPath, f)
                        item = EpisodeData(ofile)
                        self.episodes_list.append(item)
            else:
                name, file_ext = os.path.splitext(abzPath)
                if file_ext in files_extension:
                    item = EpisodeData(abzPath)
                    self.episodes_list.append(item)
        print("Found ", len(self.episodes_list), " episodes files")


def parse_parameters(self):
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="filename with list of episodes names", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    (options, args) = parser.parse_args()


if __name__ == "__main__":
    if sys.version_info.major != 2:
        raise SystemError("Use Python2")
    os.system('cls')
    "parse_parameters()"
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    else:
        args = [os.getcwd()]
    test_class = TVSeriesFileEnchancer()
    test_class.run(args)
