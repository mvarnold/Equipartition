import itertools
import numba


def dir_motif_count(network, mo_dic):

    num_motif = dict(zip(mo_dic.keys(), list(map(int, np.zeros(len(mo_dic))))))
    nodes = network.nodes()

    triplets = list(itertools.product(*[nodes, nodes, nodes]))
    triplets = [trip for trip in triplets if len(list(set(trip))) == 3]
    triplets = map(list, map(np.sort, triplets))
    u_triplets = []
    [u_triplets.append(trip) for trip in triplets if not u_triplets.count(trip)]

    for trip in u_triplets:
        sub_network = network.subgraph(trip)
        mot_match = list(map(lambda mot_id: nx.is_isomorphic(sub_network, mo_dic[mot_id]), mo_dic.keys()))
        match_keys = [mo_dic.keys()[i] for i in range(len(mo_dic)) if mot_match[i]]
        if len(match_keys) == 1:
            num_motif[match_keys[0]] += 1

    return num_motif