class Tester:
    def __init__(self, substitution_matrix = 'blosum62', fasta = "test.fasta", strategy = "global", gap_penalty = 2, verbose = False, align_out = "test_align", matrix_out = "test_matrix"):
        self.substitution_matrix = substitution_matrix
        self.fasta = fasta
        self.strategy = strategy
        self.gap_penalty = gap_penalty
        self.verbose = verbose
        self.align_out = align_out
        self.matrix_out = matrix_out
