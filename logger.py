class Logger:

    @staticmethod
    def _print(prefix, output):
        print(f'{prefix} {output}')

    def __init__(self, verbosity):
        self.verbosity = verbosity

    def info(self, output):
        if self.verbosity >= 1:
            Logger._print('INFO:', output)

    def debug(self, output):
        if self.verbosity >= 2:
            Logger._print('DEBUG:', output)

    def info_dump(self, output):
        if self.verbosity >= 3:
            Logger._print('DUMP:', output)

    
