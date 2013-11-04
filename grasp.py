from json import loads
from subprocess import PIPE, Popen

from sublime import platform, Region
from sublime_plugin import TextCommand

class GraspCommand(TextCommand):

    def run(self, crap):
        self.view.window().show_input_panel('Enter your grasp command', '',
                                            self.run_grasp, None, None)

    def run_grasp(self, raw_command):
        '''This is the workhorse of the command.'''

        if platform() == 'windows':
            command = ['grasp.cmd']
        else:
            command = ['grasp']

        # We're going to want a json object back with tons of data.
        command.extend(['-j'])
        command.extend(raw_command.split())
        command.append(self.view.file_name())

        # Run the command.
        pipe = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        result, error = pipe.communicate()

        # TODO: Handle errors.

        # Build up our selected regions.
        if result:
            self.view.sel().clear()
            for match in loads(result.decode()):
                start, stop = self.raw_to_abs(match)
                # Add it to the region.
                self.view.sel().add(Region(start, stop))

    def raw_to_abs(self, raw):
        '''
        Takes in a dict with grasp metadata,
        and returns 2-tuple of (start, stop).

        Grasp provides a very nice start and end property with each match.
        It'd be ideal to use that.
        Unfortunately, windows uses \r\n for line endings,
        and sublime may not be set up for that, so it can lead to funky errors.
        It's easier to parse the row and col and build the values from there.
        '''

        raw_start = raw['loc']['start']
        raw_end = raw['loc']['end']

        s = self.view.text_point(raw_start['line'] - 1, raw_start['column'])
        e = self.view.text_point(raw_end['line'] - 1, raw_end['column'])

        return s, e
