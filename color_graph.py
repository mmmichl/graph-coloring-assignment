"""
Main file to color graph

implementation of a optimized tabu search from the paper:
    INFORMED REACTIVE TABU SEARCH FOR GRAPH COLORING
    Porumbel, Daniel Cosmin ; Hao, Jin-Kao ; Kuntz, Pascale
    Asia-Pacific Journal of Operational Research, 25 June 2013, Vol.30(04)
"""

import argparse
from random import randint
from time import perf_counter, process_time

from col_parser import parse
from helpers import print_adj_matrix, print_matrix

DEFAULT_A = 10
DEFAULT_ALPHA = 0.6
DEFAULT_P_MAX = 1_000

MAX_ITERATIONS = 10_000_000
DEFAULT_TIMEOUT = 0  # in minutes


def main():
    parser = argparse.ArgumentParser(description='Color graphs.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files to be processed')
    parser.add_argument('--colors', dest='num_col', type=int,
                        default=17,
                        help='number of colors (default: 17)')
    parser.add_argument('--A', dest='A', type=int,
                        default=DEFAULT_A,
                        help='A of the tabu length calculation (default: %d)' % DEFAULT_A)
    parser.add_argument('--alpha', dest='alpha', type=float,
                        default=DEFAULT_ALPHA,
                        help='alpha of the tabu length calculation (default: %d)' % DEFAULT_ALPHA)
    parser.add_argument('--p-max', dest='p_max', type=int,
                        default=DEFAULT_P_MAX,
                        help='Pmax for when the reactive tl size should increase (default: %d)' % DEFAULT_P_MAX)
    parser.add_argument('--timeout', dest='timeout', type=int,
                        default=DEFAULT_TIMEOUT,
                        help='timeout in min for each k-color try; 0 to disable (default: %d min)' % DEFAULT_TIMEOUT)
    parser.add_argument('--no-opt', dest='do_opt', action="store_false",
                        default=True,
                        help='Do not try to find the minimal color, quit after finishing run with defined color')
    parser.add_argument('--re-run', dest='re_runs', type=int,
                        default=1,
                        help='How often each file should be re-run (default: 1)')

    args = parser.parse_args()

    for filename in args.files:
        for re_run in range(args.re_runs):
            sample_start_perf = perf_counter()
            process_graph(filename, args.num_col, args.timeout * 60, args.A, args.alpha, args.p_max, args.do_opt)
            print("#%d overall duration for %s: %f s\n"
                  % (re_run + 1, filename, perf_counter() - sample_start_perf))


def init_gamma(adj_matrix, gamma, init_coloring):
    """ initially calculate gamma based on the initial coloring """
    node_cnt = len(init_coloring)
    color_cnt = len(gamma[0])

    for node_idx in range(node_cnt):
        for color in range(color_cnt):
            conflict_count = 0

            for node_idx2 in range(node_cnt):
                if (node_idx != node_idx2) and adj_matrix[node_idx][node_idx2] and color == init_coloring[node_idx2]:
                    conflict_count += 1

            gamma[node_idx][color] = conflict_count


def count_conflicts(adj_matrix, init_coloring) -> int:
    """ evaluation function (Fc) """
    conflict_cnt = 0
    for idx in range(len(adj_matrix)):
        for j in range(idx):
            if adj_matrix[idx][j] and init_coloring[idx] == init_coloring[j]:
                conflict_cnt += 1

    return conflict_cnt


def process_graph(filename: str, color_cnt: int, timeout: int, A: int, alpha: float, p_max: int, do_opt: bool):
    name, node_cnt, edge_cnt, nodes = parse(filename)
    print(filename, "- read complete; nodes: %d, edges: %d, color count: %d, A: %d, alpha: %f, Pmax: %d"
          % (node_cnt, edge_cnt, color_cnt, A, alpha, p_max))

    adj_matrix = [[False for _ in range(node_cnt)] for _ in range(node_cnt)]
    for node in range(node_cnt):
        for dest_node in nodes[node]:
            adj_matrix[node][dest_node] = True

    # print()
    # print_adj_matrix(adj_matrix)

    job_done = False
    gamma = [color_cnt * [0] for _ in range(node_cnt)]

    while not job_done:
        tabu_list = [color_cnt * [0] for _ in range(node_cnt)]

        min_conflicts = 1_000_000

        print("\n== Select a random %d coloring of %d nodes" % (color_cnt, node_cnt))
        coloring = [randint(0, color_cnt - 1) for _ in range(node_cnt)]
        best_coloring = None

        init_gamma(adj_matrix, gamma, coloring)

        # print("gamma")
        # print_matrix(gamma)
        # print("coloring")
        # print_matrix([coloring])

        iter_counter = 1
        last_p_change = iter_counter
        tl_extension = 0
        start_time = perf_counter()
        old_conflict_cnt = None

        while True:
            if iter_counter % 1_000_000 == 0:
                print("  iteration", "{:_}".format(iter_counter))

            conflict_cnt = count_conflicts(adj_matrix, coloring)

            # reactive increasing of tl size
            if old_conflict_cnt == conflict_cnt:
                if last_p_change + p_max <= iter_counter:
                    last_p_change = iter_counter
                    tl_extension += 1
                    # if tl_extension == 1 or tl_extension % 20 == 0:
                    #     print("Pmax reached, increase to", tl_extension)
            else:
                last_p_change = iter_counter
                tl_extension = 0
                # if conflict_cnt < 5:
                #     print("conflict count", conflict_cnt)

            old_conflict_cnt = conflict_cnt

            # Stop criteria - moved here so the evaluation function only needs to be run once
            if conflict_cnt < min_conflicts:
                min_conflicts = conflict_cnt
                best_coloring = coloring.copy()

                # if conflict_cnt < 10:
                #     print("%d conflicts at iteration %d after %d s"
                #           % (min_conflicts, iter_counter, perf_counter() - start_time))

                if conflict_cnt == 0 and color_cnt <= 3:
                    job_done = True
                    return best_coloring
                elif conflict_cnt == 0:
                    break

            best_delta = 1_000_000

            for n in range(node_cnt):
                for c in range(color_cnt):
                    if c != coloring[n]:
                        delta = gamma[n][c] - gamma[n][coloring[n]]

                        if delta < best_delta:
                            # if not tabu OR if Aspiration criterion is met: found a new all-time best
                            if tabu_list[n][c] < iter_counter or delta + conflict_cnt < min_conflicts:
                                best_node = n
                                best_color = c
                                best_delta = delta

            assert (best_node is not None)
            # tabu length
            tl = round(alpha * conflict_cnt) + randint(1, A) + tl_extension
            color_tabu = coloring[best_node]
            tabu_list[best_node][color_tabu] = tl + iter_counter
            coloring[best_node] = best_color

            # update gamma to new coloring
            for idx, g in enumerate(gamma):
                if adj_matrix[idx][best_node]:
                    g[color_tabu] -= 1
                    g[best_color] += 1

            iter_counter += 1
            if iter_counter == MAX_ITERATIONS:
                print("Max iteration count reached (%d), aborting search" % MAX_ITERATIONS)
                return None

            if (perf_counter() - start_time) > timeout:
                print("Timeout reached (%d), aborting search" % timeout)
                return None

        print("Found solution within %f min" % ((perf_counter() - start_time) / 60.))
        # print_matrix([best_coloring])
        if not do_opt:
            return best_coloring

        color_cnt -= 1

    return coloring


if __name__ == "__main__":
    # execute only if run as a script
    main()
