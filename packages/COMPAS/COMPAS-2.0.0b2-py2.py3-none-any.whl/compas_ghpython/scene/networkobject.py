from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import NetworkObject as BaseNetworkObject
from .sceneobject import GHSceneObject


class NetworkObject(GHSceneObject, BaseNetworkObject):
    """Scene object for drawing network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A COMPAS network.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, network, **kwargs):
        super(NetworkObject, self).__init__(network=network, **kwargs)

    def draw(self):
        """Draw the entire network with default color settings.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`]
            List of created Rhino geometries.
        """
        self._guids = self.draw_edges() + self.draw_nodes()
        return self.guids

    def draw_nodes(self, nodes=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes: list[hashable], optional
            The selection of nodes that should be drawn.
            Default is None, in which case all nodes are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        for node in nodes or self.network.nodes():  # type: ignore
            points.append(conversions.point_to_rhino(self.node_xyz[node]))

        return points

    def draw_edges(self, edges=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        lines = []

        for edge in edges or self.network.edges():  # type: ignore
            lines.append(conversions.line_to_rhino((self.node_xyz[edge[0]], self.node_xyz[edge[1]])))

        return lines
