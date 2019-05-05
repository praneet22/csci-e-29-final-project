"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mfinal_project` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``final_project.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``final_project.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
from final_project.tasks.stylize_task import PreProcessVideo
from final_project.tasks.prepare_batch import PrepareAzureBatchCPU, PrepareAzureBatchGPU
from luigi import build


def main(args=None):

    build([PrepareAzureBatchCPU(),PrepareAzureBatchGPU()], local_scheduler=True)
    # print("The Stylized image for {} is generated: {}".format(args.image, args.output))
    print("The Stylized video for is generated:".format())
