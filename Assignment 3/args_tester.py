class Tester:
    def __init__(self, command, fasta, transition, emission, verbosity, out_dir, max_iter, conv_thresh):
        self.command = command
        self.fasta = fasta
        self.transition = transition
        self.emission = emission
        self.verbosity = verbosity
        self.out_dir = out_dir
        self.max_iter = max_iter
        self.conv_thresh = conv_thresh