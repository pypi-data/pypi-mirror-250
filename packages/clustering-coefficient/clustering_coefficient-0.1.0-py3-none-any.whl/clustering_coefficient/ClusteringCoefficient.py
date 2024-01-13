# When the plugin development is finished, you can copy the associated
# Python file to /Users/melancon/.Tulip-5.7/plugins/python
# and it will be automatically loaded at Tulip startup

from tulip import tlp
import tulipplugins


class ClusteringCoefficient(tlp.DoubleAlgorithm):
    def __init__(self, context):
        tlp.DoubleAlgorithm.__init__(self, context)
        # You can add parameters to the plugin here through the
        # following syntax:
        # self.add<Type>Parameter('<paramName>', '<paramDoc>',
        #                         '<paramDefaultValue>')
        # (see the documentation of class tlp.WithParameter to see what
        #  parameter types are supported).

    def _node_neighborhood_(self, node):
        return set([n.id for n in self.graph.getInOutNodes(node)])

    def node_coefficient(self, node):
        neighbours = [n for n in self.graph.getInOutNodes(node)]
        degree = len(neighbours)
        fof = 0
        for i in range(1, degree):
            for j in range(i):
                if neighbours[i].id in self.nodes_neighborhoods[neighbours[j].id]:
                    fof += 1
        try:
            return 2 * fof / (degree * (degree - 1))
        except ZeroDivisionError:  # node has degree 0 or 1
            return fof

    def check(self):
        # This method is called before applying the algorithm on the
        # input graph. You can perform some precondition checks here.
        # See comments in the run method to know how to have access to
        # the input graph.
        #
        # Must return a tuple (Boolean, string). First member indicates if the
        # algorithm can be applied and the second one can be used to provide
        # an error message.
        return (True, "")

    def run(self):
        # This method is the entry point of the algorithm when it is called
        # and must contain its implementation.
        #
        # The graph on which the algorithm is applied can be accessed through
        # the 'graph' class attribute (see documentation of class tlp.Graph).
        #
        # The parameters provided by the user are stored in a dictionary
        # that can be accessed through the 'dataSet' class attribute.
        #
        # The result of this double algorithm must be stored in the
        # double property accessible through the 'result' class attribute
        # (see documentation to know how to work with graph properties).
        #
        # The method must return a Boolean indicating if the algorithm
        # has been successfully applied on the input graph.
        self.nodes_neighborhoods = {
            n.id: self._node_neighborhood_(n) for n in self.graph.getNodes()
        }
        clustering_coefficient = self.dataSet["result"]
        for n in self.graph.getNodes():
            clustering_coefficient[n] = self.node_coefficient(n)
        return True


# The line below does the magic to register the plugin into the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup(
    "ClusteringCoefficient",
    "Clustering Coefficient",
    "G.M.",
    "21/11/2023",
    "Computes the clustering coefficient of nodes as defined by Watts and Strogatz 1998",
    "1.0",
    "Graph",
)
