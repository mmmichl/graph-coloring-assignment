"""
Commandline Wrapper for SMAC tool

A full call by SMAC looks like this:
    <algo>                 <instance> <instance specific> <cutoff time>  <runlength> <seed> <algorithm parameters>
    python smac_wrapper.py 0          0                   99999999999999 0           12345  --A 10 --alpha 0.6 --colors 7 --p-max 1000

"""
import argparse
import sys
from time import perf_counter

from color_graph import process_graph

DEFAULT_A = 10
DEFAULT_ALPHA = 0.6
DEFAULT_P_MAX = 1_000

if __name__ == '__main__':
    # Unused in this example:
    instance, instance_specific, cutoff, runlength = sys.argv[1:5]
    seed = sys.argv[5]
    # sys.argv[6] and sys.argv[8] are the names of the target algorithm
    # parameters (here: "-x1", "-x2")

    parser = argparse.ArgumentParser(description='Wrapper for SMAC.')
    parser.add_argument('instance')
    parser.add_argument('instance_specific')
    parser.add_argument('cutoff')
    parser.add_argument('runlength')
    parser.add_argument('seed')
    # parser.add_argument('--colors', dest='num_col', type=int,
    #                     default=17,
    #                     help='number of colors (default: 17)')
    parser.add_argument('--A', dest='A', type=int,
                        default=DEFAULT_A,
                        help='A of the tabu length calculation (default: %d)' % DEFAULT_A)
    parser.add_argument('--alpha', dest='alpha', type=float,
                        default=DEFAULT_ALPHA,
                        help='alpha of the tabu length calculation (default: %d)' % DEFAULT_ALPHA)
    parser.add_argument('--p-max', dest='p_max', type=int,
                        default=DEFAULT_P_MAX,
                        help='Pmax for when the reactive tl size should increase (default: %d)' % DEFAULT_P_MAX)

    args = parser.parse_args()

    instance_ks = {
        "data/DSJC125.1.col": 7,
        "data/DSJC125.5.col": 26,
        "data/DSJC250.1.col": 14,
        "data/DSJC250.5.col": 49,
    }
    start_perf = perf_counter()
    result, run_length = process_graph(args.instance,
                                       instance_ks[args.instance],
                                       int(float(cutoff)),
                                       args.A,
                                       args.alpha,
                                       args.p_max,
                                       False,
                                       0)
    exec_time = perf_counter() - start_perf

    if result:
        print('Result for SMAC: SUCCESS, %d, %d, 1, %s' % (int(exec_time), run_length, seed))
    else:
        print('Result for SMAC: TIMEOUT, %d, %d, 0, %s' % (int(exec_time), run_length, seed))
