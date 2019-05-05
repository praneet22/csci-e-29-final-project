import io
import os
import random
from contextlib import contextmanager
from luigi.format import FileWrapper
from luigi.local_target import LocalTarget, atomic_file
from pathlib import PurePath

class suffix_preserving_atomic_file(atomic_file):
    """Modification of the original atomic_file class. This class
    writes to a temp file and moves it on close(). Also cleans up the temp file if
close is not invoked."""

    def generate_tmp_path(self, path):
        '''Overriding the method generate_tmp_path from atomic_file class to add functionality
         to manage the same file extension for tmp and final file.
        '''
        exts = list(map(lambda x: x.lstrip('.'), PurePath(path).suffixes))
        file_name = list(set(path.split('.')) - set(exts))[0]
        return '{}-luigi-tmp-{}.{}'.format(file_name, random.randrange(0, 1e10), '.'.join(exts))

class BaseAtomicProviderLocalTarget(LocalTarget):

    atomic_provider = atomic_file

    def __init__(self, path, format=None, is_tmp=False):
        super(BaseAtomicProviderLocalTarget, self).__init__(path, format, is_tmp)

    def open(self, mode='r'):
        rwmode = mode.replace('b', '').replace('t', '')
        if rwmode == 'w':
            self.makedirs()

            tmp_file_path = self.atomic_provider(self.path)

            print('tmp_file_path:', tmp_file_path.name)

            return self.format.pipe_writer(tmp_file_path)

        elif rwmode == 'r':
            fileobj = FileWrapper(io.BufferedReader(io.FileIO(self.path, mode)))
            return self.format.pipe_reader(fileobj)

        else:
            raise Exception("mode must be 'r' or 'w' (got: {})".format(mode))

    @contextmanager
    def temporary_path(self):
        self.makedirs()
        with self.atomic_provider(self.path) as af:
            yield af.tmp_path

class SuffixPreservingLocalTarget(BaseAtomicProviderLocalTarget):
    atomic_provider = suffix_preserving_atomic_file