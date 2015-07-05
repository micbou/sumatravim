from __future__ import absolute_import, division, print_function

import sys
import argparse
import subprocess
#import win32ui
#import dde
from .dde import dde
from distutils.spawn import find_executable


class Sumatra():
    def __init__(self, pdf, servername = 'GVIM'):
        self.pdf = pdf
        self.servername = servername
        self.CreateServer()


    def CreateServer(self):
        connected = self.Connect()
        if not connected:
            self.Create()
            try_number = 1
            while not connected:
                connected = self.Connect()
                if try_number > 5:
                    raise RuntimeError('Number of tries to connect to '
                                       'a Sumatra instance exceeded.')
        #server = dde.CreateServer()
        #server.Create('Vim')

        #self.conversation = dde.CreateConversation(server)
        #connected = self.Connect()
        #if not connected:
        #    self.Create()
        #    try_number = 1
        #    while not connected:
        #        connected = self.Connect()
        #        if try_number > 5:
        #            raise RuntimeError('Number of tries to connect to '
        #                               'a Sumatra instance exceeded.')

            # By starting SumatraPDF from Vim, the focus is lost in Vim, so
            # it is forced back.
            self.FocusVim()


    def FocusVim(self):
        gvim_cmd = ['gvim',
                    '--servername', self.servername,
                    '--remote-send', '<C-c>:call foreground() | echo<CR>']
        subprocess.Popen(gvim_cmd)


    def Connect(self):
        try:
            self.conversation = dde.DDEClient('SUMATRA', 'control')
        except dde.DDEError:
        #    self.conversation.ConnectTo('SUMATRA', 'control')
        #except Exception:
            return False
        return True


    def Create(self):
        executable = find_executable('SumatraPDF')
        cmd = [executable, self.pdf, '-inverse-search']
        cmd.append('gvim --servername ' + self.servername + ' --remote-send '
                   '"<C-c>:execute \'drop \' . escape(\'%f\', \' \') | '
                   ':call foreground() | echo<CR>%lGzvzz"')

        subprocess.Popen(cmd)



    def Open(self):
        cmd = '[Open("' + self.pdf + '", 0, 0, 0)]'
        self.conversation.execute(cmd)
        #self.conversation.Exec(cmd)

        # Though we use a DDE command, the focus is lost when the file is not
        # already open so it is forced back.
        self.FocusVim()


    def ForwardSearch(self, tex, line):
        cmd = ( '[ForwardSearch("' +
                self.pdf + '","' +
                tex + '",' +
                line +
                ', 0, 0, 0)]' )
        self.conversation.execute(cmd)
        #self.conversation.Exec(cmd)


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


def CallSumatra(args):
    sumatra = Sumatra(args.pdf, args.servername)

    sumatra.Open()

    if args.forward_search:
        sumatra.ForwardSearch(args.forward_search[0],
                              args.forward_search[1])


def Main():
    """
    SumatraPDF wrapper
    """
    args = ParseArguments()
    CallSumatra(args)


if __name__ == '__main__':
    sys.exit(Main())
