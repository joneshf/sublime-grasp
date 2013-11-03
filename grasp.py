import itertools as it
import operator as op
from subprocess import PIPE, Popen

from sublime import platform, Region
import sublime_plugin

class GraspCommand(sublime_plugin.TextCommand):

    def run(self, crap):
        self.view.window().show_input_panel('Enter your grasp command', '',
                                            self.run_grasp, None, None)

    def run_grasp(self, raw_command):
        '''This is the workhorse of the command.'''

        if platform() == 'windows':
            command = ['grasp.cmd']
        else:
            command = ['grasp']

        # Need the line/columns, but don't want the color.
        command.extend(['-n', '-b', '--color=false'])
        command.extend(raw_command.split())
        command.append(self.view.file_name())

        # Run the command.
        pipe = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1)
        result, error = pipe.communicate()

        # TODO: Handle errors.
        # TODO: This only seems to return one line,
        # instead of many as you get when running this form the shell.

        # Rip out the lines from our result.
        raw_lines = map(lambda s: ''.join(it.takewhile(lambda r: r != ':', s)),
                        result.decode().split('\n'))
        # Get rid of blanks.
        lines = filter(None, raw_lines)
        # Build up our selected regions.
        for line in lines:
            self.view.sel().clear()
            raw_start, raw_stop = line.split('-')
            start = self.raw_to_abs(raw_start)
            # Off by one.
            stop = self.raw_to_abs(raw_stop) + 1
            # Add it to the region.
            self.view.sel().add(Region(start, stop))

    def raw_to_abs(self, row_col):
        '''
        Takes in a string of the form 'r,c',
        where r is the row and c is the column,
        and returns an absolute position.
        '''

        return reduce(op.mul, map(int, row_col.split(',')))
