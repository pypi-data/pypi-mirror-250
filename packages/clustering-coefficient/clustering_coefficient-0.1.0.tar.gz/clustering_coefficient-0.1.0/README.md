# Clustering Coefficient
This script allows to compute Watts & Strogatz's clustering coefficient of nodes in a graph $G = (V, E)$. It is defined as the edge density of the graph induced from neighbors of a node, relatively to a clique of comparable size. More precisely, given a node $u \in V$, denoting its set of neighbors as $N_G(u)$, the clustering coefficient of $u$ is equal to:

$C_G(u) = \frac{|E(N_G(u))|}{d(d-1)/2}$

where $d = |N_G(u)|$ is the degree of node $u$ (its number $|N_G(u)|$ of neighbors).

## Installing and using the plugin

The library relies on [`tulip-python`](https://pypi.org/project/tulip-python/), a python binding of the [C++ Graph Visualization framework Tulip](https://tulip.labri.fr/). Tulip also comes as a GUI.

Several libraries need to be installed prior to using the plugin, that can for instance be installed running `poetry install --no-root`. The specific dependencies are listed as part of the `pyproject.toml` file. A simple test script can optionally be run.

The plugin itself is typically used as:
```
# assuming a graph as already been defined
params = tlp.getDefaultPluginParameters('Clustering Coefficient', graph)
clustering = graph.getDoubleProperty('clustering coeff')
params['result'] = clustering
graph.applyDoubleAlgorithm('Broker score', clustering, params)
```
Alternatively, the plugin may be used within the Tulip GUI after the script has been loaded and ran.