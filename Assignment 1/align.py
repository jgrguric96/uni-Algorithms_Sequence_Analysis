#!/usr/bin/python3

"""
DESCRIPTION:
    Template code for the Dynamic Programming assignment in the Algorithms in Sequence Analysis course at the VU.
    
INSTRUCTIONS:
    Complete the code (compatible with Python 3!) upload to CodeGrade via corresponding Canvas assignment.

AUTHOR:
    Name: Josip Grguric
    StudentID: 2704719
"""



import argparse
import pickle



def parse_args():
    "Parses inputs from commandline and returns them as a Namespace object."

    parser = argparse.ArgumentParser(prog = 'python3 align.py',
        formatter_class = argparse.RawTextHelpFormatter, description =
        '  Aligns the first two sequences in a specified FASTA\n'
        '  file with a chosen strategy and parameters.\n'
        '\n'
        'defaults:\n'
        '  strategy = global\n'
        '  substitution matrix = pam250\n'
        '  gap penalty = 2')
        
    parser.add_argument('fasta', help='path to a FASTA formatted input file')
    parser.add_argument('output', nargs='*', 
        help='path to an output file where the alignment is saved\n'
             '  (if a second output file is given,\n'
             '   save the score matrix in there)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
        help='print the score matrix and alignment on screen', default=False)
    parser.add_argument('-s', '--strategy', dest='strategy',
        choices=['global','semiglobal','local'], default="global")
    parser.add_argument('-m', '--matrix', dest='substitution_matrix',
        choices=['pam250','blosum62','identity'], default='pam250')
    parser.add_argument('-g', '--gap_penalty', dest='gap_penalty', type=int,
        help='must be a positive integer', default=2)

    args = parser.parse_args()

    args.align_out = args.output[0] if args.output else False
    args.matrix_out = args.output[1] if len(args.output) >= 2 else False
                      # Fancy inline if-else statements. Use cautiously!
                      
    if args.gap_penalty <= 0:
        parser.error('gap penalty must be a positive integer')

    return args



def load_substitution_matrix(name):
    "Loads and returns the specified substitution matrix from a pickle (.pkl) file."
    # Substitution matrices have been prepared as nested dictionaries:
    # the score of substituting A for Z can be found with subst['A']['Z']
    # NOTE: Only works if working directory contains the correct folder and file!
    
    with open('substitution_matrices/%s.pkl' % name, 'rb') as f:
        subst = pickle.load(f)
    return subst
    
    

def load_sequences(filepath):
    "Reads a FASTA file and returns the first two sequences it contains."
    
    seq1 = []
    seq2 = []
    with open(filepath,'r') as f:
        for line in f:
            if line.startswith('>'):
                if not seq1:
                    current_seq = seq1
                elif not seq2:
                    current_seq = seq2
                else:
                    break # Stop if a 3rd sequence is encountered
            else:
                current_seq.append(line.strip())
    
    if not seq2:
        raise Exception('Error: Not enough sequences in specified FASTA file.')
    
    seq1 = ''.join(seq1)
    seq2 = ''.join(seq2)
    return seq1, seq2



def align(seq1, seq2, strategy, substitution_matrix, gap_penalty):
    "Do pairwise alignment using the specified strategy and parameters."
    # This function consists of 3 parts:
    #
    #   1) Initialize a score matrix as a "list of lists" of the appropriate length.
    #      Fill in the correct values for the first row and column given the strategy.
    #        (local / semiglobal = 0  --  global = stacking gap penalties)
    #   2) Fill in the rest of the score matrix using Dynamic Programming, accounting
    #      for the selected alignment strategy, substitution matrix and gap penalty.
    #   3) Perform the correct traceback routine on your filled in score matrix.
    #
    # Both the resulting alignment (sequences with gaps and the corresponding score)
    # and the filled in score matrix are returned as outputs.
    #
    # NOTE: You are strongly encouraged to think about how you can reuse (parts of)
    #       your code between steps 2 and 3 for the different strategies!


    ### 1: Initialize
    M = len(seq1)+1
    N = len(seq2)+1
    score_matrix = []
    for i in range(M):
        row = []
        score_matrix.append(row)
        for j in range(N):
            row.append(0)

    if strategy == 'global':
        #####################
        # START CODING HERE #
        #####################
        # Used vals: (seq1, seq2, strategy, substitution_matrix, gap_penalty)
        # Three points:
        # 1. Change values in first row and column according to strategy. (separate func)
        # 2. Perform forward steps / calculation over matrix (this is a separate func)
        # 3. Perform backward steps to get best alignment over both sequences (use high roads)
        step_matrix = {}
        for i in range(0, M):
            if i:
                score_matrix[i][0] = score_matrix[i-1][0] - gap_penalty
                step_matrix[(i,0)] = [(i-1, 0)]
        for i in range(0, N):
            if i:
                score_matrix[0][i] = score_matrix[0][i-1] - gap_penalty
                step_matrix[(0, i)] = [(0, i-1)]  # Change the zeroes in the first row and column to the correct values.
        #####################
        #  END CODING HERE  #
        #####################



    ### 2: Fill in Score Matrix

    #####################
    # START CODING HERE #
    #####################

    # I would keep track of all paths, but given that we are only interested in high road I will prioritize that.
    # This might need to be re-written depending on strategy. Works for global as is.
    def dp_function(scores, steps_matrix, X, Y):
        steps = []

        # Semi-global gap penalty changes
        # I am so confused by the results of pam250 and identity substitutions
        disallow_gap_X, disallow_gap_Y = 0, 0
        # if strategy != "global":
        #     if X == 2: disallow_gap_X = -99999
        #     if Y == 2: disallow_gap_Y = -99999

        # 12:00 : this path is easily selected if we select first value in dict
        max_value = scores[Y-1][X] - gap_penalty + disallow_gap_Y
        steps.append((Y-1, X))

        # 10:30
        current_value = scores[Y-1][X-1] + substitution_matrix.get(seq1[Y-1]).get(seq2[X-1])
        if current_value >= max_value:
            if current_value > max_value:
                max_value = current_value
                steps = []
            steps.append((Y-1, X-1))

        # 09:00 : this path is also easily selected if we select the last value in dict
        current_value = scores[Y][X-1] - gap_penalty + disallow_gap_X
        if current_value >= max_value:
            if current_value > max_value:
                max_value = current_value
                # Issue appeared here. Forgot to reset list to 0
                steps = []
            steps.append((Y, X-1))

        steps_matrix[(Y, X)] = steps
        return max_value

    try: step_matrix
    except NameError:
        step_matrix = {}
        for i in range(0, M):
            if i:
                step_matrix[(i,0)] = [(i-1, 0)]
        for i in range(0, N):
            if i:
                step_matrix[(0, i)] = [(0, i-1)]
    for i in range(1,M):
        for j in range(1,N):
            score_matrix[i][j] = dp_function(score_matrix, step_matrix, j, i)

    #####################
    #  END CODING HERE  #
    #####################   


    ### 3: Traceback

    #####################
    # START CODING HERE #
    #####################

    def get_alignments(Y, X):
        """
            Def: Gets alignment coordinates and picks highest road it can \n
            Returns: sequences
        """
        if not step_matrix.get((Y, X)):
            return ("", "")

        highest_road = step_matrix.get((Y, X))[0]

        sequences = get_alignments(highest_road[0], highest_road[1])
        if highest_road[0] == Y:
            sequences = (sequences[0] + "-", sequences[1] + seq2[X-1])
        elif highest_road[1] == X:
            sequences = (sequences[0] + seq1[Y-1], sequences[1] + "-")
        else:
            sequences = (sequences[0] + seq1[Y-1], sequences[1] + seq2[X-1])

        return sequences

    score_max = score_matrix[M - 1][N - 1]
    score_max_M, score_max_N = M - 1, N - 1
    starts_at = "last column"

    #TODO: Do i just do look for highest cell in both row and column?
    if strategy == "semiglobal":

        for i in range(0, M-1):
            if score_matrix[i][N-1] >= score_max:
                if score_matrix[i][N-1] > score_max or i < score_max_M:
                    score_max = score_matrix[i][N-1]
                    score_max_M = i
                    score_max_N = N - 1
                    starts_at = "last column"

        for i in range(N-1, -1, -1):
            if score_matrix[M-1][i] > score_max:
                score_max = score_matrix[M-1][i]
                score_max_N = i
                score_max_M = M - 1
                starts_at = "last row"

    sequences = get_alignments(score_max_M, score_max_N)

    if starts_at == "last row":
        diff = len(seq2) - score_max_N
        sequences = (sequences[0] + '-'*diff,
                     sequences[1] + seq2[len(seq2) - diff:])
    else:
        diff = len(seq1) - score_max_M
        sequences = (sequences[0] + seq1[len(seq1) - diff:],
                     sequences[1] + '-'*diff)


    aligned_seq1 = sequences[0]  # These are dummy values! Change the code so that
    aligned_seq2 = sequences[1]  # aligned_seq1 and _seq2 contain the input sequences
    align_score = score_matrix[score_max_M][score_max_N]       # with gaps inserted at the appropriate positions.

    #####################
    #  END CODING HERE  #
    #####################   


    alignment = (aligned_seq1, aligned_seq2, align_score)
    return (alignment, score_matrix)



def print_score_matrix(s1,s2,mat):
    "Pretty print function for a score matrix."
    
    # Prepend filler characters to seq1 and seq2
    s1 = '-' + s1
    s2 = ' -' + s2
    
    # Print them around the score matrix, in columns of 5 characters
    print(''.join(['%5s' % aa for aa in s2])) # Convert s2 to a list of length 5 strings, then join it back into a string
    for i,row in enumerate(mat):               # Iterate through the rows of your score matrix (and keep count with 'i').
        vals = ['%5i' % val for val in row]    # Convert this row's scores to a list of strings.
        vals.insert(0,'%5s' % s1[i])           # Add this row's character from s2 to the front of the list
        print(''.join(vals))                   # Join the list elements into a single string, and print the line.



def print_alignment(a):
    "Pretty print function for an alignment (and alignment score)."
    
    # Unpack the alignment tuple
    seq1 = a[0]
    seq2 = a[1]
    score = a[2]
    
    # Check which positions are identical
    match = ''
    for i in range(len(seq1)): # Remember: Aligned sequences have the same length!
        match += '|' if seq1[i] == seq2[i] else ' ' # Fancy inline if-else statement. Use cautiously!
            
    # Concatenate lines into a list, and join them together with newline characters.
    print('\n'.join([seq1,match,seq2,'','Score = %i' % score]))



def save_alignment(a,f):
    "Saves two aligned sequences and their alignment score to a file."
    with open(f,'w') as out:
        out.write(a[0] + '\n') # Aligned sequence 1
        out.write(a[1] + '\n') # Aligned sequence 2
        out.write('Score: %i' % a[2]) # Alignment score


    
def save_score_matrix(m,f):
    "Saves a score matrix to a file in tab-separated format."
    with open(f,'w') as out:
        for row in m:
            vals = [str(val) for val in row]
            out.write('\t'.join(vals)+'\n')
    


def main(args = False):
    # Process arguments and load required data
    if not args: args = parse_args()
    
    sub_mat = load_substitution_matrix(args.substitution_matrix)
    seq1, seq2 = load_sequences(args.fasta)

    # Perform specified alignment
    strat = args.strategy
    gp = args.gap_penalty
    alignment, score_matrix = align(seq1, seq2, strat, sub_mat, gp)

    # If running in "verbose" mode, print additional output
    if args.verbose:
        print_score_matrix(seq1,seq2,score_matrix)
        print('') # Insert a blank line in between
        print_alignment(alignment)
    
    # Save results
    if args.align_out: save_alignment(alignment, args.align_out)
    if args.matrix_out: save_score_matrix(score_matrix, args.matrix_out)



if __name__ == '__main__':
    #TESTING
    #TODO Delete arg_tester class and py. Do not want to risk getting a lower grade.

    #TODO Issues remaining:

    #TODO Issues fixed:
    # Fix problem where recursion ends before final characters (or the opposite)
    # Actually looking at it this seems to be the biggest problem causer
    # double checking seems to lead to following conclusion: i am not selecting best path
    # semi-glob works
    from args_tester import Tester
    test = Tester(fasta="test2.fasta", strategy="semiglobal", gap_penalty=4, substitution_matrix='pam250', matrix_out="test2_matrix", align_out="test2_align")
    main(test)

 # 5,11 Y and X values
 # 5, 10 as well