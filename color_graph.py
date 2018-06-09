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

A = 10
alpha = 0.6
MAX_ITERATIONS = 10_000_000
TIMEOUT = 1 * 60    # in seconds


def main():
    parser = argparse.ArgumentParser(description='Color graphs.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files to be processed')
    parser.add_argument('--colors', dest='num_col', type=int,
                        default=17,
                        help='number of colors (default: 17)')

    args = parser.parse_args()

    for filename in args.files:
        sample_start_perf = perf_counter()
        process_graph(filename, args.num_col)
        print("overall duration for %s: %f s\n"
              % (filename, perf_counter() - sample_start_perf))


def init_gamma(adj_matrix, gamma, init_coloring):
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
    conflict_cnt = 0
    for idx in range(len(adj_matrix)):
        for j in range(idx):
            if adj_matrix[idx][j] and init_coloring[idx] == init_coloring[j]:
                conflict_cnt += 1

    return conflict_cnt


def process_graph(filename: str, color_cnt: int):
    name, node_cnt, edge_cnt, nodes = parse(filename)
    print(filename, "- read complete; nodes:", node_cnt, " edges:", edge_cnt, " color count:", color_cnt)

    adj_matrix = [[False for _ in range(node_cnt)] for _ in range(node_cnt)]
    for node in range(node_cnt):
        for dest_node in nodes[node]:
            adj_matrix[node][dest_node] = True

    # print()
    # print_adj_matrix(adj_matrix)
    print()

    job_done = False
    gamma = [color_cnt * [0] for _ in range(node_cnt)]

    while not job_done:
        tabu_list = [color_cnt * [0] for _ in range(node_cnt)]

        min_conflicts = 1_000_000

        print("\nSelect a random %d coloring of %d nodes" % (color_cnt, node_cnt))
        init_coloring = [randint(0, color_cnt-1) for _ in range(node_cnt)]

        init_gamma(adj_matrix, gamma, init_coloring)

        # print("gamma")
        # print_matrix(gamma)
        # print("init_coloring")
        # print_matrix([init_coloring])

        iter_counter = 1
        while iter_counter < MAX_ITERATIONS:
            if iter_counter % 1_000_000 == 0:
                print("iteration", iter_counter)

            conflict_cnt = count_conflicts(adj_matrix, init_coloring)
            # print("conflict count", conflict_cnt)

            if conflict_cnt < min_conflicts and conflict_cnt < 10:
                min_conflicts = conflict_cnt
                print("%d conflicts at iteration %d" % (min_conflicts, iter_counter))
                if conflict_cnt == 0 and color_cnt <= 3:
                    job_done = True
                    return init_coloring
                elif conflict_cnt == 0:
                    break

            best_delta = 1_000_000

            for n in range(node_cnt):
                for c in range(color_cnt):
                    if c != init_coloring[n]:
                        delta = gamma[n][c] - gamma[n][init_coloring[n]]

                        if delta < best_delta:
                            if tabu_list[n][c] < iter_counter \
                                    or (tabu_list[n][c] >= iter_counter and delta + conflict_cnt == 0):
                                best_node = n
                                best_color = c
                                best_delta = delta

            assert(best_node is not None)
            tl = alpha * conflict_cnt + randint(1, A)
            color_tabu = init_coloring[best_node]
            tabu_list[best_node][color_tabu] = tl + iter_counter
            init_coloring[best_node] = best_color

            for idx, g in enumerate(gamma):
                if adj_matrix[idx][best_node]:
                    g[color_tabu] -= 1
                    g[best_color] += 1

            iter_counter += 1
            if iter_counter == MAX_ITERATIONS:
                print("Max iteration count reached (%d), aborting search" % MAX_ITERATIONS)
                return init_coloring

        color_cnt -= 1

    return init_coloring


if __name__ == "__main__":
    # execute only if run as a script
    main()
