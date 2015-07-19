from __future__ import absolute_import, division, print_function

import argparse
import subprocess
from distutils.spawn import find_executable

SUMATRAPDF_NOT_FOUND_MESSAGE = ( 'SumatraPDF executable not found. '
                                 'You should add it to the PATH.' )
GVIM_NOT_FOUND_MESSAGE = ( 'Gvim executable not found. '
                           'You should add it to the PATH.' )
VIM_FOCUS_RETRIES_NUMBER = 5


class SumatraVim():
    def __init__(self, pdf, servername = 'GVIM'):
        self.pdf = pdf
        self.sumatraPDF = find_executable('SumatraPDF')
        if not self.sumatraPDF:
            raise RuntimeError(SUMATRAPDF_NOT_FOUND_MESSAGE)
        self.gvim = find_executable('gvim')
        if not self.gvim:
            raise RuntimeError(GVIM_NOT_FOUND_MESSAGE)
        self.servername = servername


    def Open(self):
        return self.Execute()


    def ForwardSearch(self, tex, line):
        return self.Execute('-forward-search', tex, line)


    def ForceFocusVim(self):
        retries = VIM_FOCUS_RETRIES_NUMBER
        while retries > 0:
            self.FocusVim()
            retries = retries - 1


    def FocusVim(self):
        gvim_cmd = [
            self.gvim,
            '--servername', self.servername,
            '--remote-send', ':<C-E><C-U>call foreground() | echo<CR>'
        ]
        subprocess.call(gvim_cmd)



    def Execute(self, *args):
        full_cmd = [self.sumatraPDF, self.pdf,
                    '-reuse-instance', '-inverse-search']
        full_cmd.append(
            self.gvim + ' --servername ' +
            self.servername + ' --remote-send '
            '":<C-E><C-U>:execute \'drop \' . escape(\'%f\', \' \') | '
            ':call foreground() | echo<CR>%lGzvzz"'
        )
        full_cmd.extend(list(args))

        self.proc = subprocess.Popen(full_cmd)


def ParseArguments():
    parser = argparse.ArgumentParser(
        description = 'SumatraVim, a SumatraPDF wrapper to improve '
                      'interaction between Vim, LaTeX, and SumatraPDF.')
    parser.add_argument('--servername', default='GVIM',
                        metavar='servername',
                        help='Vim server name (default: %(default)s)')
    parser.add_argument('--forward-search', nargs=2,
                        metavar=('tex', 'line'),
                        help='Forward search')
    parser.add_argument('pdf',
                        help='PDF file')
    return parser.parse_args()


def CallSumatraVim(args):
    sumatra_vim = SumatraVim(args.pdf, args.servername)

    if args.forward_search:
        sumatra_vim.ForwardSearch(args.forward_search[0],
                                  args.forward_search[1])
        sumatra_vim.ForceFocusVim()
        return

    sumatra_vim.Open()
    sumatra_vim.ForceFocusVim()


def Main():
    """
    SumatraVim, a SumatraPDF wrapper to improve
    interaction between Vim, LaTeX, and SumatraPDF.
    """
    args = ParseArguments()
    CallSumatraVim(args)
