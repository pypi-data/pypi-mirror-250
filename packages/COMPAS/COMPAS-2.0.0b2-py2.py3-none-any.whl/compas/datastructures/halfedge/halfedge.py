from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import sample

from compas.topology import breadth_first_traverse
from compas.topology import connected_components

from compas.datastructures.datastructure import Datastructure
from compas.datastructures.attributes import VertexAttributeView
from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView

from compas.utilities import pairwise
from compas.utilities import window


class HalfEdge(Datastructure):
    """Base half-edge data structure for representing the topology of open oor closed surface meshes.

    Parameters
    ----------
    default_vertex_attributes: dict, optional
        Default values for vertex attributes.
    default_edge_attributes: dict, optional
        Default values for edge attributes.
    default_face_attributes: dict, optional
        Default values for face attributes.
    **kwargs : dict, optional
        Additional attributes to add to the data structure.

    Attributes
    ----------
    attributes : dict[str, Any]
        General attributes of the data structure that are included in the data representation and serialization.
    default_vertex_attributes : dict[str, Any]
        Dictionary containing default values for the attributes of vertices.
        It is recommended to add a default to this dictionary using :meth:`update_default_vertex_attributes`
        for every vertex attribute used in the data structure.
    default_edge_attributes : dict[str, Any]
        Dictionary containing default values for the attributes of edges.
        It is recommended to add a default to this dictionary using :meth:`update_default_edge_attributes`
        for every edge attribute used in the data structure.
    default_face_attributes : dict[str, Any]
        Dictionary contnaining default values for the attributes of faces.
        It is recommended to add a default to this dictionary using :meth:`update_default_face_attributes`
        for every face attribute used in the data structure.

    See Also
    --------
    :class:`compas.datastructures.Mesh`

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "dva": {"type": "object"},
            "dea": {"type": "object"},
            "dfa": {"type": "object"},
            "vertex": {
                "type": "object",
                "patternProperties": {"^[0-9]+$": {"type": "object"}},
                "additionalProperties": False,
            },
            "face": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "array",
                        "items": {"type": "integer", "minimum": 0},
                        "minItems": 3,
                    }
                },
                "additionalProperties": False,
            },
            "facedata": {
                "type": "object",
                "patternProperties": {"^[0-9]+$": {"type": "object"}},
                "additionalProperties": False,
            },
            "edgedata": {
                "type": "object",
                "patternProperties": {"^\\([0-9]+, [0-9]+\\)$": {"type": "object"}},
                "additionalProperties": False,
            },
            "max_vertex": {"type": "integer", "minimum": -1},
            "max_face": {"type": "integer", "minimum": -1},
        },
        "required": [
            "dva",
            "dea",
            "dfa",
            "vertex",
            "face",
            "facedata",
            "edgedata",
            "max_vertex",
            "max_face",
        ],
    }

    def __init__(
        self, default_vertex_attributes=None, default_edge_attributes=None, default_face_attributes=None, **kwargs
    ):
        super(HalfEdge, self).__init__(**kwargs)
        self._max_vertex = -1
        self._max_face = -1
        self.vertex = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self.edgedata = {}
        self.default_vertex_attributes = {}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}
        if default_vertex_attributes:
            self.default_vertex_attributes.update(default_vertex_attributes)
        if default_edge_attributes:
            self.default_edge_attributes.update(default_edge_attributes)
        if default_face_attributes:
            self.default_face_attributes.update(default_face_attributes)

    def __str__(self):
        tpl = "<HalfEdge with {} vertices, {} faces, {} edges>"
        return tpl.format(self.number_of_vertices(), self.number_of_faces(), self.number_of_edges())

    # --------------------------------------------------------------------------
    # Data
    # --------------------------------------------------------------------------

    @property
    def data(self):
        return {
            "dva": self.default_vertex_attributes,
            "dea": self.default_edge_attributes,
            "dfa": self.default_face_attributes,
            "vertex": {str(vertex): attr for vertex, attr in self.vertex.items()},
            "face": {str(face): vertices for face, vertices in self.face.items()},
            "facedata": {str(face): attr for face, attr in self.facedata.items()},
            "edgedata": self.edgedata,
            "max_vertex": self._max_vertex,
            "max_face": self._max_face,
        }

    @classmethod
    def from_data(cls, data):
        dva = data.get("dva") or {}
        dfa = data.get("dfa") or {}
        dea = data.get("dea") or {}

        halfedge = cls(default_vertex_attributes=dva, default_face_attributes=dfa, default_edge_attributes=dea)

        vertex = data.get("vertex") or {}
        face = data.get("face") or {}
        facedata = data.get("facedata") or {}
        edgedata = data.get("edgedata") or {}

        for key, attr in iter(vertex.items()):
            halfedge.add_vertex(key=key, attr_dict=attr)

        for fkey, vertices in iter(face.items()):
            attr = facedata.get(fkey) or {}
            halfedge.add_face(vertices, fkey=fkey, attr_dict=attr)

        halfedge.edgedata = edgedata

        halfedge._max_vertex = data.get("max_vertex", halfedge._max_vertex)
        halfedge._max_face = data.get("max_face", halfedge._max_face)

        return halfedge

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def adjacency(self):
        return self.halfedge

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the mesh data.

        Returns
        -------
        None

        """
        del self.vertex
        del self.edgedata
        del self.halfedge
        del self.face
        del self.facedata
        self.vertex = {}
        self.edgedata = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self._max_vertex = -1
        self._max_face = -1

    def vertex_sample(self, size=1):
        """A random sample of the vertices.

        Parameters
        ----------
        size : int, optional
            The number of vertices in the random sample.

        Returns
        -------
        list[int]
            The identifiers of the vertices.

        See Also
        --------
        :meth:`edge_sample`, :meth:`face_sample`

        """
        return sample(list(self.vertices()), size)

    def edge_sample(self, size=1):
        """A random sample of the edges.

        Parameters
        ----------
        size : int, optional
            The number of edges in the random sample.

        Returns
        -------
        list[tuple[int, int]]
            The identifiers of the edges.

        See Also
        --------
        :meth:`vertex_sample`, :meth:`face_sample`

        """
        return sample(list(self.edges()), size)

    def face_sample(self, size=1):
        """A random sample of the faces.

        Parameters
        ----------
        size : int, optional
            The number of faces in the random sample.

        Returns
        -------
        list[int]
            The identifiers of the faces.

        See Also
        --------
        :meth:`vertex_sample`, :meth:`edge_sample`

        """
        return sample(list(self.faces()), size)

    def vertex_index(self):
        """Returns a dictionary that maps vertex identifiers to the
        corresponding index in a vertex list or array.

        Returns
        -------
        dict[int, int]
            A dictionary of vertex-index pairs.

        See Also
        --------
        :meth:`index_vertex`

        """
        return {key: index for index, key in enumerate(self.vertices())}

    def index_vertex(self):
        """Returns a dictionary that maps the indices of a vertex list to
        the corresponding vertex identifiers.

        Returns
        -------
        dict[int, int]
            A dictionary of index-vertex pairs.

        See Also
        --------
        :meth:`vertex_index`

        """
        return dict(enumerate(self.vertices()))

    # --------------------------------------------------------------------------
    # Builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex to the mesh object.

        Parameters
        ----------
        key : int, optional
            The vertex identifier.
        attr_dict : dict[str, Any], optional
            A dictionary of vertex attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The identifier of the vertex.

        See Also
        --------
        :meth:`add_face`
        :meth:`delete_vertex`, :meth:`delete_face`

        Notes
        -----
        If no key is provided for the vertex, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        0
        >>> mesh.add_vertex(x=0, y=0, z=0)
        1
        >>> mesh.add_vertex(key=2)
        2
        >>> mesh.add_vertex(key=0, x=1)
        0

        """
        if key is None:
            key = self._max_vertex = self._max_vertex + 1
        key = int(key)
        if key > self._max_vertex:
            self._max_vertex = key
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self.vertex[key].update(attr)
        return key

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the mesh object.

        Parameters
        ----------
        vertices : list[int]
            A list of vertex keys.
        attr_dict : dict[str, Any], optional
            A dictionary of face attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        See Also
        --------
        :meth:`add_vertex`
        :meth:`delete_face`, :meth:`delete_vertex`

        Returns
        -------
        int
            The key of the face.

        Raises
        ------
        TypeError
            If the provided face key is of an unhashable type.

        Notes
        -----
        If no key is provided for the face, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """
        if vertices[-1] == vertices[0]:
            vertices = vertices[:-1]
        vertices = [int(key) for key in vertices]
        vertices[:] = [u for u, v in pairwise(vertices + vertices[:1]) if u != v]
        if len(vertices) < 3:
            return
        if fkey is None:
            fkey = self._max_face = self._max_face + 1
        fkey = int(fkey)
        if fkey > self._max_face:
            self._max_face = fkey
        attr = attr_dict or {}
        attr.update(kwattr)
        self.face[fkey] = vertices
        self.facedata.setdefault(fkey, attr)
        for u, v in pairwise(vertices + vertices[:1]):
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
        return fkey

    # --------------------------------------------------------------------------
    # Modifiers
    # --------------------------------------------------------------------------

    def delete_vertex(self, key):
        """Delete a vertex from the mesh and everything that is attached to it.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_face`
        :meth:`add_vertex`, :meth:`add_face`

        Notes
        -----
        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        """
        nbrs = self.vertex_neighbors(key)
        for nbr in nbrs:
            fkey = self.halfedge[key][nbr]
            if fkey is None:
                continue
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = None
            del self.face[fkey]
            if fkey in self.facedata:
                del self.facedata[fkey]
        for nbr in nbrs:
            del self.halfedge[nbr][key]
            edge = "-".join(map(str, sorted([nbr, key])))
            if edge in self.edgedata:
                del self.edgedata[edge]
        for nbr in nbrs:
            for n in self.vertex_neighbors(nbr):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
                    edge = "-".join(map(str, sorted([nbr, n])))
                    if edge in self.edgedata:
                        del self.edgedata[edge]
        del self.halfedge[key]
        del self.vertex[key]

    def delete_face(self, fkey):
        """Delete a face from the mesh object.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_vertex`
        :meth:`add_vertex`, :meth:`add_face`

        Notes
        -----
        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        """
        for u, v in self.face_halfedges(fkey):
            if self.halfedge[u][v] == fkey:
                # if the halfedge still points to the face
                # this might not be the case of the deletion is executed
                # during the procedure of adding a new (replacement) face
                self.halfedge[u][v] = None
                if self.halfedge[v][u] is None:
                    del self.halfedge[u][v]
                    del self.halfedge[v][u]
                    edge = "-".join(map(str, sorted([u, v])))
                    if edge in self.edgedata:
                        del self.edgedata[edge]
        del self.face[fkey]
        if fkey in self.facedata:
            del self.facedata[fkey]

    def remove_unused_vertices(self):
        """Remove all unused vertices from the mesh object.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_vertex`

        """
        for u in list(self.vertices()):
            if u not in self.halfedge:
                del self.vertex[u]
            else:
                if not self.halfedge[u]:
                    del self.vertex[u]
                    del self.halfedge[u]

    cull_vertices = remove_unused_vertices

    def flip_cycles(self):
        """Flip the cycle directions of all faces.

        Returns
        -------
        None
            The mesh is modified in place.

        Notes
        -----
        This function does not care about the directions being unified or not. It
        just reverses whatever direction it finds.

        """
        self.halfedge = {key: {} for key in self.vertices()}
        for fkey in self.faces():
            self.face[fkey][:] = self.face[fkey][::-1]
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = fkey
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

    # --------------------------------------------------------------------------
    # Accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the mesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex identifier.
            If `data` is True, the next vertex as a (key, attr) tuple.

        See Also
        --------
        :meth:`faces`, :meth:`edges`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key in self.vertex:
            if not data:
                yield key
            else:
                yield key, self.vertex_attributes(key)

    def faces(self, data=False):
        """Iterate over the faces of the mesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face identifier.
            If `data` is True, the next face as a (fkey, attr) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`edges`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key in self.face:
            if not data:
                yield key
            else:
                yield key, self.face_attributes(key)

    def edges(self, data=False):
        """Iterate over the edges of the mesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a ((u, v), data) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`faces`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        Notes
        -----
        Mesh edges have no topological meaning. They are only used to store data.
        Edges are not automatically created when vertices and faces are added to
        the mesh. Instead, they are created when data is stored on them, or when
        they are accessed using this method.

        This method yields the directed edges of the mesh.
        Unless edges were added explicitly using :meth:`add_edge` the order of
        edges is *as they come out*. However, as long as the toplogy remains
        unchanged, the order is consistent.

        """
        seen = set()
        for u in self.halfedge:
            for v in self.halfedge[u]:
                key = u, v
                ikey = v, u
                if key in seen or ikey in seen:
                    continue
                seen.add(key)
                seen.add(ikey)
                if not data:
                    yield key
                else:
                    yield key, self.edge_attributes(key)

    def vertices_where(self, conditions=None, data=False, **kwargs):
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

        See Also
        --------
        :meth:`faces_where`, :meth:`edges_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`faces_where_predicate`

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key, attr in self.vertices(True):
            is_match = True
            attr = attr or {}

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(key)

                    if isinstance(val, list):
                        if value not in val:
                            is_match = False
                            break
                        break

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if val < minval or val > maxval:
                            is_match = False
                            break
                    else:
                        if value != val:
                            is_match = False
                            break

                else:
                    if name not in attr:
                        is_match = False
                        break

                    if isinstance(attr[name], list):
                        if value not in attr[name]:
                            is_match = False
                            break
                        break

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if attr[name] < minval or attr[name] > maxval:
                            is_match = False
                            break
                    else:
                        if value != attr[name]:
                            is_match = False
                            break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def vertices_where_predicate(self, predicate, data=False):
        """Get vertices for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the vertex identifier and the vertex attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

        See Also
        --------
        :meth:`faces_where_predicate`, :meth:`edges_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key, attr in self.vertices(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def edges_where(self, conditions=None, data=False, **kwargs):
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        See Also
        --------
        :meth:`vertices_where`, :meth:`faces_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`faces_where_predicate`

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key in self.edges():
            is_match = True

            attr = self.edge_attributes(key) or {}

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(key)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def edges_where_predicate(self, predicate, data=False):
        """Get edges for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 3 parameters:
            the identifier of the first vertex, the identifier of the second vertex, and the edge attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition ot the vertex identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        See Also
        --------
        :meth:`faces_where_predicate`, :meth:`vertices_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key, attr in self.edges(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def faces_where(self, conditions=None, data=False, **kwargs):
        """Get faces for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the face attributes in addition to face identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

        See Also
        --------
        :meth:`vertices_where`, :meth:`edges_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`faces_where_predicate`

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for fkey in self.faces():
            is_match = True

            attr = self.face_attributes(fkey) or {}

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(fkey)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield fkey, attr
                else:
                    yield fkey

    def faces_where_predicate(self, predicate, data=False):
        """Get faces for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the face identifier and the face attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

        See Also
        --------
        :meth:`edges_where_predicate`, :meth:`vertices_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for fkey, attr in self.faces(True):
            if predicate(fkey, attr):
                if data:
                    yield fkey, attr
                else:
                    yield fkey

    # --------------------------------------------------------------------------
    # Attributes
    # --------------------------------------------------------------------------

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """Update the default vertex attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_edge_attributes`
        :meth:`update_default_face_attributes`

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)

    def vertex_attribute(self, key, name, value=None):
        """Get or set an attribute of a vertex.

        Parameters
        ----------
        key : int
            The vertex identifier.
        name : str
            The name of the attribute
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute,
            or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        :meth:`vertex_attributes`, :meth:`vertices_attribute`, :meth:`vertices_attributes`
        :meth:`unset_vertex_attribute`
        :meth:`edge_attribute`
        :meth:`face_attribute`

        """
        if key not in self.vertex:
            raise KeyError(key)
        if value is not None:
            self.vertex[key][name] = value
            return None
        if name in self.vertex[key]:
            return self.vertex[key][name]
        else:
            if name in self.default_vertex_attributes:
                return self.default_vertex_attributes[name]

    def unset_vertex_attribute(self, key, name):
        """Unset the attribute of a vertex.

        Parameters
        ----------
        key : int
            The vertex identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        :meth:`vertex_attribute`, :meth:`vertex_attributes`, :meth:`vertices_attribute`, :meth:`vertices_attributes`
        :meth:`unset_edge_attribute`
        :meth:`unset_face_attribute`

        Notes
        -----
        Unsetting the value of a vertex attribute implicitly sets it back to the value
        stored in the default vertex attribute dict.

        """
        if name in self.vertex[key]:
            del self.vertex[key][name]

    def vertex_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            the function returns a dictionary of all attribute name-value pairs of the vertex.
            If the parameter `names` is not empty,
            the function returns a list of the values corresponding to the requested attribute names.
            The function returns None if it is used as a "setter".

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        :meth:`vertex_attribute`, :meth:`vertices_attribute`, :meth:`vertices_attributes`
        :meth:`edge_attributes`
        :meth:`face_attributes`

        """
        if key not in self.vertex:
            raise KeyError(key)
        if names and values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self.vertex[key][name] = value
            return
        # use it as a getter
        if not names:
            # return all vertex attributes as a dict
            return VertexAttributeView(self.default_vertex_attributes, self.vertex[key])
        values = []
        for name in names:
            if name in self.vertex[key]:
                values.append(self.vertex[key][name])
            elif name in self.default_vertex_attributes:
                values.append(self.default_vertex_attributes[name])
            else:
                values.append(None)
        return values

    def vertices_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[int], optional
            A list of vertex identifiers.

        Returns
        -------
        list[Any] | None
            The value of the attribute for each vertex,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the vertices does not exist.

        See Also
        --------
        :meth:`vertex_attribute`, :meth:`vertex_attributes`, :meth:`vertices_attributes`
        :meth:`edges_attribute`
        :meth:`faces_attribute`

        """
        if not keys:
            keys = self.vertices()
        if value is not None:
            for key in keys:
                self.vertex_attribute(key, name, value)
            return
        return [self.vertex_attribute(key, name) for key in keys]

    def vertices_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple vertices.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
        values : list[Any], optional
            The values of the attributes.
        keys : list[int], optional
            A list of vertex identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            the function returns a list containing an attribute dict per vertex.
            If the parameter `names` is not empty,
            the function returns a list containing a list of attribute values per vertex corresponding to the provided attribute names.
            The function returns None if it is used as a "setter".

        Raises
        ------
        KeyError
            If any of the vertices does not exist.

        See Also
        --------
        :meth:`vertex_attribute`, :meth:`vertex_attributes`, :meth:`vertices_attribute`
        :meth:`edges_attributes`
        :meth:`faces_attributes`

        """
        if not keys:
            keys = self.vertices()
        if values is not None:
            for key in keys:
                self.vertex_attributes(key, names, values)
            return
        return [self.vertex_attributes(key, names) for key in keys]

    def update_default_face_attributes(self, attr_dict=None, **kwattr):
        """Update the default face attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_vertex_attributes`
        :meth:`update_default_edge_attributes`

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_face_attributes.update(attr_dict)

    def face_attribute(self, key, name, value=None):
        """Get or set an attribute of a face.

        Parameters
        ----------
        key : int
            The face identifier.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`face_attributes`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`unset_face_attribute`
        :meth:`edge_attribute`
        :meth:`vertex_attribute`

        """
        if key not in self.face:
            raise KeyError(key)
        if value is not None:
            if key not in self.facedata:
                self.facedata[key] = {}
            self.facedata[key][name] = value
            return
        if key in self.facedata and name in self.facedata[key]:
            return self.facedata[key][name]
        if name in self.default_face_attributes:
            return self.default_face_attributes[name]

    def unset_face_attribute(self, key, name):
        """Unset the attribute of a face.

        Parameters
        ----------
        key : int
            The face identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`face_attributes`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`unset_edge_attribute`
        :meth:`unset_vertex_attribute`

        Notes
        -----
        Unsetting the value of a face attribute implicitly sets it back to the value
        stored in the default face attribute dict.

        """
        if key not in self.face:
            raise KeyError(key)
        if key in self.facedata:
            if name in self.facedata[key]:
                del self.facedata[key][name]

    def face_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a face.

        Parameters
        ----------
        key : int
            The identifier of the face.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            a dictionary of all attribute name-value pairs of the face.
            If the parameter `names` is not empty,
            a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`edge_attributes`
        :meth:`vertex_attributes`

        """
        if key not in self.face:
            raise KeyError(key)
        if names and values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                if key not in self.facedata:
                    self.facedata[key] = {}
                self.facedata[key][name] = value
            return
        # use it as a getter
        if not names:
            return FaceAttributeView(self.default_face_attributes, self.facedata.setdefault(key, {}))
        values = []
        for name in names:
            value = self.face_attribute(key, name)
            values.append(value)
        return values

    def faces_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple faces.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[int], optional
            A list of face identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per face of the requested attribute,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`face_attributes`, :meth:`faces_attributes`
        :meth:`edges_attribute`
        :meth:`vertices_attribute`

        """
        if not keys:
            keys = self.faces()
        if value is not None:
            for key in keys:
                self.face_attribute(key, name, value)
            return
        return [self.face_attribute(key, name) for key in keys]

    def faces_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple faces.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        keys : list[int], optional
            A list of face identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per face an attribute dict with all attributes (default + custom) of the face.
            If the parameter `names` is not empty,
            a list containing per face a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`face_attributes`, :meth:`faces_attribute`
        :meth:`edges_attributes`
        :meth:`vertices_attributes`

        """
        if not keys:
            keys = self.faces()
        if values is not None:
            for key in keys:
                self.face_attributes(key, names, values)
            return
        return [self.face_attributes(key, names) for key in keys]

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_vertex_attributes`
        :meth:`update_default_face_attributes`

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    def edge_attribute(self, edge, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge as a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        :meth:`edge_attributes`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`unset_edge_attribute`
        :meth:`vertex_attribute`
        :meth:`face_attribute`

        """
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if value is not None:
            if key not in self.edgedata:
                self.edgedata[key] = {}
            self.edgedata[key][name] = value
            return
        if key in self.edgedata and name in self.edgedata[key]:
            return self.edgedata[key][name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def unset_edge_attribute(self, edge, name):
        """Unset the attribute of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edge_attributes`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`unset_vertex_attribute`
        :meth:`unset_face_attribute`

        Notes
        -----
        Unsetting the value of an edge attribute implicitly sets it back to the value
        stored in the default edge attribute dict.

        """
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if key in self.edgedata and name in self.edgedata[key]:
            del self.edgedata[key][name]

    def edge_attributes(self, edge, names=None, values=None):
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            a dictionary of all attribute name-value pairs of the edge.
            If the parameter `names` is not empty,
            a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`vertex_attributes`
        :meth:`face_attributes`

        """
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        if names and values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self.edge_attribute(edge, name, value)
            return
        # use it as a getter
        if not names:
            key = str(tuple(sorted(edge)))
            # get the entire attribute dict
            return EdgeAttributeView(self.default_edge_attributes, self.edgedata.setdefault(key, {}))
        # get only the values of the named attributes
        values = []
        for name in names:
            value = self.edge_attribute(edge, name)
            values.append(value)
        return values

    def edges_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[tuple[int, int]], optional
            A list of edge identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per edge of the requested attribute,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edge_attributes`, :meth:`edges_attributes`
        :meth:`vertex_attributes`
        :meth:`face_attributes`

        """
        edges = keys or self.edges()
        if value is not None:
            for edge in edges:
                self.edge_attribute(edge, name, value)
            return
        return [self.edge_attribute(edge, name) for edge in edges]

    def edges_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        keys : list[tuple[int, int]], optional
            A list of edge identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per edge an attribute dict with all attributes (default + custom) of the edge.
            If the parameter `names` is not empty,
            a list containing per edge a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edge_attributes`, :meth:`edges_attribute`
        :meth:`vertex_attributes`
        :meth:`face_attributes`

        """
        edges = keys or self.edges()
        if values is not None:
            for edge in edges:
                self.edge_attributes(edge, names, values)
            return
        return [self.edge_attributes(edge, names) for edge in edges]

    # --------------------------------------------------------------------------
    # Info
    # --------------------------------------------------------------------------

    def summary(self):
        """Print a summary of the mesh.

        Returns
        -------
        str
            The formatted summary text.

        """
        tpl = "\n".join(
            [
                "{} summary",
                "=" * (len(self.name) + len(" summary")),
                "- vertices: {}",
                "- edges: {}",
                "- faces: {}",
            ]
        )
        return tpl.format(
            self.name,
            self.number_of_vertices(),
            self.number_of_edges(),
            self.number_of_faces(),
        )

    def number_of_vertices(self):
        """Count the number of vertices in the mesh.

        Returns
        -------
        int

        See Also
        --------
        :meth:`number_of_edges`
        :meth:`number_of_faces`

        """
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Count the number of edges in the mesh.

        Returns
        -------
        int

        See Also
        --------
        :meth:`number_of_vertices`
        :meth:`number_of_faces`

        """
        return len(list(self.edges()))

    def number_of_faces(self):
        """Count the number of faces in the mesh.

        Returns
        -------
        int

        See Also
        --------
        :meth:`number_of_vertices`
        :meth:`number_of_edges`

        """
        return len(list(self.faces()))

    def is_valid(self):
        """Verify that the mesh is valid.

        A mesh is valid if the following conditions are fulfilled:

        * halfedges don't point at non-existing faces
        * all vertices are in the halfedge dict
        * there are no None-None halfedges
        * all faces have corresponding halfedge entries

        Returns
        -------
        bool
            True, if the mesh is valid.
            False, otherwise.

        See Also
        --------
        :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        for key in self.vertices():
            if key not in self.halfedge:
                return False

        for u in self.halfedge:
            if u not in self.vertex:
                return False
            for v in self.halfedge[u]:
                if v not in self.vertex:
                    return False
                if self.halfedge[u][v] is None and self.halfedge[v][u] is None:
                    return False
                fkey = self.halfedge[u][v]
                if fkey is not None:
                    if fkey not in self.face:
                        return False

        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if u not in self.vertex:
                    return False
                if v not in self.vertex:
                    return False
                if u not in self.halfedge:
                    return False
                if v not in self.halfedge[u]:
                    return False
                if fkey != self.halfedge[u][v]:
                    return False
        return True

    def is_regular(self):
        """Verify that the mesh is regular.

        A mesh is regular if the following conditions are fulfilled:

        * All faces have the same number of edges.
        * All vertices have the same degree, i.e. they are incident to the same number of edges.

        Returns
        -------
        bool
            True, if the mesh is regular.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if not self.vertex or not self.face:
            return False

        vkey = self.vertex_sample(size=1)[0]
        degree = self.vertex_degree(vkey)

        for vkey in self.vertices():
            if self.vertex_degree(vkey) != degree:
                return False

        fkey = self.face_sample(size=1)[0]
        vcount = len(self.face_vertices(fkey))

        for fkey in self.faces():
            vertices = self.face_vertices(fkey)
            if len(vertices) != vcount:
                return False

        return True

    def is_manifold(self):
        """Verify that the mesh is manifold.

        A mesh is manifold if the following conditions are fulfilled:

        * Each edge is incident to only one or two faces.
        * The faces incident to a vertex form a closed or an open fan.

        Returns
        -------
        bool
            True, if the mesh is manifold.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if not self.vertex:
            return False

        for key in self.vertices():
            if list(self.halfedge[key].values()).count(None) > 1:
                return False

            nbrs = self.vertex_neighbors(key, ordered=True)

            if not nbrs:
                return False

            if self.halfedge[nbrs[0]][key] is None:
                for nbr in nbrs[1:-1]:
                    if self.halfedge[key][nbr] is None:
                        return False

                if self.halfedge[key][nbrs[-1]] is not None:
                    return False
            else:
                for nbr in nbrs[1:]:
                    if self.halfedge[key][nbr] is None:
                        return False

        return True

    def is_orientable(self):
        """Verify that the mesh is orientable.

        A manifold mesh is orientable if any two adjacent faces have compatible orientation,
        i.e. the faces have a unified cycle direction.

        Returns
        -------
        bool
            True, if the mesh is orientable.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        raise NotImplementedError

    def is_trimesh(self):
        """Verify that the mesh consists of only triangles.

        Returns
        -------
        bool
            True, if the mesh is a triangle mesh.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_quadmesh`

        """
        if not self.face:
            return False
        return not any(3 != len(self.face_vertices(fkey)) for fkey in self.faces())

    def is_quadmesh(self):
        """Verify that the mesh consists of only quads.

        Returns
        -------
        bool
            True, if the mesh is a quad mesh.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`

        """
        if not self.face:
            return False
        return not any(4 != len(self.face_vertices(fkey)) for fkey in self.faces())

    def is_empty(self):
        """Verify that the mesh is empty.

        Returns
        -------
        bool
            True if the mesh has no vertices.
            False otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if self.number_of_vertices() == 0:
            return True
        return False

    def is_closed(self):
        """Verify that the mesh is closed.

        Returns
        -------
        bool
            True if the mesh is not empty and has no naked edges.
            False otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if self.is_empty():
            return False
        for edge in self.edges():
            if self.is_edge_on_boundary(edge):
                return False
        return True

    def is_connected(self):
        """Verify that the mesh is connected.

        Returns
        -------
        bool
            True if the mesh is not empty and has no naked edges.
            False otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if not self.vertex:
            return False
        nodes = breadth_first_traverse(self.adjacency, self.vertex_sample(size=1)[0])
        return len(nodes) == self.number_of_vertices()

    def euler(self):
        """Calculate the Euler characteristic.

        Returns
        -------
        int
            The Euler characteristic.

        See Also
        --------
        :meth:`genus`

        """
        V = len([vkey for vkey in self.vertices() if len(self.vertex_neighbors(vkey)) != 0])
        E = self.number_of_edges()
        F = self.number_of_faces()
        return V - E + F

    # --------------------------------------------------------------------------
    # Components
    # --------------------------------------------------------------------------

    def connected_vertices(self):
        """Find groups of connected vertices.

        Returns
        -------
        list[list[int]]
            Groups of connected vertices.

        """
        return connected_components(self.adjacency)

    def connected_faces(self):
        """Find groups of connected faces.

        Returns
        -------
        list[list[int]]
            Groups of connected faces.

        """
        # return connected_components(self.face_adjacency)
        parts = self.connected_vertices()
        return [set([face for vertex in part for face in self.vertex_faces(vertex)]) for part in parts]

    # --------------------------------------------------------------------------
    # Vertex topology
    # --------------------------------------------------------------------------

    def has_vertex(self, key):
        """Verify that a vertex is in the mesh.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the mesh.
            False otherwise.

        """
        return key in self.vertex

    def is_vertex_connected(self, key):
        """Verify that a vertex is connected.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is connected to at least one other vertex.
            False otherwise.

        """
        return self.vertex_degree(key) > 0

    def is_vertex_on_boundary(self, key):
        """Verify that a vertex is on a boundary.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is on the boundary.
            False otherwise.

        """
        for nbr in self.halfedge[key]:
            if self.halfedge[key][nbr] is None:
                return True
        return False

    def vertex_neighbors(self, key, ordered=False):
        """Return the neighbors of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        ordered : bool, optional
            If True, return the neighbors in the cycling order of the faces.

        Returns
        -------
        list[int]
            The list of neighboring vertices.
            If the vertex lies on the boundary of the mesh,
            an ordered list always starts and ends with with boundary vertices.

        Notes
        -----
        Due to the nature of the ordering algorithm, the neighbors cycle around
        the node in the opposite direction as the cycling direction of the faces.
        For some algorithms this produces the expected results. For others it doesn't.
        For example, a dual mesh constructed relying on these conventions will have
        oposite face cycle directions compared to the original.

        """
        temp = list(self.halfedge[key])
        if not ordered:
            return temp
        if not temp:
            return temp
        if len(temp) == 1:
            return temp
        # if one of the neighbors points to the *outside* face
        # start there
        # otherwise the starting point can be random
        start = temp[0]
        for nbr in temp:
            if self.halfedge[key][nbr] is None:
                start = nbr
                break
        # start in the opposite direction
        # to avoid pointing at an *outside* face again
        fkey = self.halfedge[start][key]
        nbrs = [start]
        count = 1000
        while count:
            count -= 1
            nbr = self.face_vertex_descendant(fkey, key)
            fkey = self.halfedge[nbr][key]
            if nbr == start:
                break
            nbrs.append(nbr)
            if fkey is None:
                break
        return nbrs

    def vertex_neighborhood(self, key, ring=1):
        """Return the vertices in the neighborhood of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        ring : int, optional
            The number of neighborhood rings to include.

        Returns
        -------
        list[int]
            The vertices in the neighborhood.

        Notes
        -----
        The vertices in the neighborhood are unordered.

        """
        nbrs = set(self.vertex_neighbors(key))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for key in nbrs:
                temp += self.vertex_neighbors(key)
            nbrs.update(temp)
            i += 1
        return nbrs

    def vertex_degree(self, key):
        """Count the neighbors of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        int
            The degree of the vertex.

        """
        return len(self.vertex_neighbors(key))

    def vertex_min_degree(self):
        """Compute the minimum degree of all vertices.

        Returns
        -------
        int
            The lowest degree of all vertices.

        """
        if not self.vertex:
            return 0
        return min(self.vertex_degree(key) for key in self.vertices())

    def vertex_max_degree(self):
        """Compute the maximum degree of all vertices.

        Returns
        -------
        int
            The highest degree of all vertices.

        """
        if not self.vertex:
            return 0
        return max(self.vertex_degree(key) for key in self.vertices())

    def vertex_faces(self, key, ordered=False, include_none=False):
        """The faces connected to a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        ordered : bool, optional
            If True, return the faces in cycling order.
        include_none : bool, optional
            If True, include *outside* faces in the list.

        Returns
        -------
        list[int]
            The faces connected to a vertex.

        """
        if not ordered:
            faces = list(self.halfedge[key].values())
        else:
            nbrs = self.vertex_neighbors(key, ordered=True)
            faces = [self.halfedge[key][n] for n in nbrs]
        if include_none:
            return faces
        return [fkey for fkey in faces if fkey is not None]

    # --------------------------------------------------------------------------
    # Edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, key):
        """Verify that the mesh contains a specific edge.

        Warnings
        --------
        This method may produce unexpected results.

        Parameters
        ----------
        key : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.

        """
        return key in set(self.edges())

    def has_halfedge(self, key):
        """Verify that a halfedge is part of the mesh.

        Parameters
        ----------
        key : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        bool
            True if the halfedge is part of the mesh.
            False otherwise.

        """
        u, v = key
        return u in self.halfedge and v in self.halfedge[u]

    def edge_faces(self, edge):
        """Find the two faces adjacent to an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        tuple[int, int]
            The identifiers of the adjacent faces.
            If the edge is on the boundary, one of the identifiers is None.

        """
        u, v = edge
        return self.halfedge[u][v], self.halfedge[v][u]

    def halfedge_face(self, edge):
        """Find the face corresponding to a halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        int | None
            The identifier of the face corresponding to the halfedge.
            None, if the halfedge is on the outside of a boundary.

        Raises
        ------
        KeyError
            If the halfedge does not exist.

        """
        u, v = edge
        return self.halfedge[u][v]

    def is_edge_on_boundary(self, edge):
        """Verify that an edge is on the boundary.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge is on the boundary.
            False otherwise.

        """
        u, v = edge
        return self.halfedge[v][u] is None or self.halfedge[u][v] is None

    # --------------------------------------------------------------------------
    # Polyedge topology
    # --------------------------------------------------------------------------

    def edge_loop(self, edge):
        """Find all edges on the same loop as a given edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        u, v = edge
        uv_loop = self.halfedge_loop((u, v))
        if uv_loop[0][0] == uv_loop[-1][1]:
            return uv_loop
        vu_loop = self.halfedge_loop((v, u))
        vu_loop[:] = [(u, v) for v, u in vu_loop[::-1]]
        return vu_loop + uv_loop[1:]

    def halfedge_loop(self, edge):
        """Find all edges on the same loop as the halfedge, in the direction of the halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        if self.is_edge_on_boundary(edge):
            return self._halfedge_loop_on_boundary(edge)
        edges = [edge]
        u, v = edge
        while True:
            nbrs = self.vertex_neighbors(v, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(u)
            u = v
            v = nbrs[i - 2]
            edges.append((u, v))
            if v == edges[0][0]:
                break
        return edges

    def _halfedge_loop_on_boundary(self, edge):
        """Find all edges on the same loop as the halfedge, in the direction of the halfedge, if the halfedge is on the boundary.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        edges = [edge]
        u, v = edge
        while True:
            nbrs = self.vertex_neighbors(v)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == u:
                    continue
                if self.is_edge_on_boundary((v, temp)):
                    nbr = temp
                    break
            if nbr is None:
                break
            u, v = v, nbr
            edges.append((u, v))
            if v == edges[0][0]:
                break
        return edges

    def edge_strip(self, edge, return_faces=False):
        """Find all edges on the same strip as a given edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.
        return_faces : bool, optional
            Return the faces on the strip in addition to the edges.

        Returns
        -------
        list[tuple[int, int]] | tuple[list[tuple[int, int]], list[int]]
            If `return_faces` is False, the edges on the same strip as the given edge.
            If `return_faces` is False, the edges on the same strip and the corresponding faces.

        """
        u, v = edge
        if self.halfedge[v][u] is None:
            strip = self.halfedge_strip((u, v))
        elif self.halfedge[u][v] is None:
            edges = self.halfedge_strip((v, u))
            strip = [(u, v) for v, u in edges[::-1]]
        else:
            vu_strip = self.halfedge_strip((v, u))
            vu_strip[:] = [(u, v) for v, u in vu_strip[::-1]]
            if vu_strip[0] == vu_strip[-1]:
                strip = vu_strip
            else:
                uv_strip = self.halfedge_strip((u, v))
                strip = vu_strip[:-1] + uv_strip
        if not return_faces:
            return strip
        faces = [self.halfedge_face(edge) for edge in strip[:-1]]
        return strip, faces

    def halfedge_strip(self, edge):
        """Find all edges on the same strip as a given halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same strip as the given halfedge.

        """
        u, v = edge
        edges = [edge]
        while True:
            face = self.halfedge[u][v]
            if face is None:
                break
            vertices = self.face_vertices(face)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
            edges.append((u, v))
            if (u, v) == edge:
                break
        return edges

    # --------------------------------------------------------------------------
    # Face topology
    # --------------------------------------------------------------------------

    def has_face(self, fkey):
        """Verify that a face is part of the mesh.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        """
        return fkey in self.face

    def face_vertices(self, fkey):
        """The vertices of a face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[int]
            Ordered vertex identifiers.

        """
        return self.face[fkey]

    def face_halfedges(self, fkey):
        """The halfedges of a face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of a face.

        """
        vertices = self.face_vertices(fkey)
        return list(pairwise(vertices + vertices[0:1]))

    def face_corners(self, fkey):
        """Return triplets of face vertices forming the corners of the face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[int]
            The corners of the face in the form of a list of vertex triplets.

        """
        vertices = self.face_vertices(fkey)
        return list(window(vertices + vertices[0:2], 3))

    def face_neighbors(self, fkey):
        """Return the neighbors of a face across its edges.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[int]
            The identifiers of the neighboring faces.

        """
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def face_neighborhood(self, key, ring=1):
        """Return the faces in the neighborhood of a face.

        Parameters
        ----------
        key : int
            The identifier of the face.
        ring : int, optional
            The size of the neighborhood.

        Returns
        -------
        list[int]
            A list of face identifiers.

        """
        nbrs = set(self.face_neighbors(key))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for key in nbrs:
                temp += self.face_neighbors(key)
            nbrs.update(temp)
            i += 1
        return list(nbrs)

    def face_degree(self, fkey):
        """Count the neighbors of a face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        int
            The count.

        """
        return len(self.face_neighbors(fkey))

    def face_min_degree(self):
        """Compute the minimum degree of all faces.

        Returns
        -------
        int
            The lowest degree.

        """
        if not self.face:
            return 0
        return min(self.face_degree(fkey) for fkey in self.faces())

    def face_max_degree(self):
        """Compute the maximum degree of all faces.

        Returns
        -------
        int
            The highest degree.

        """
        if not self.face:
            return 0
        return max(self.face_degree(fkey) for fkey in self.faces())

    def face_vertex_ancestor(self, fkey, key, n=1):
        """Return the n-th vertex before the specified vertex in a specific face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.
        key : int
            The identifier of the vertex.
        n : int, optional
            The index of the vertex ancestor.
            Default is 1, meaning the previous vertex.

        Returns
        -------
        int
            The identifier of the vertex before the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        i = self.face[fkey].index(key)
        return self.face[fkey][(i - n) % len(self.face[fkey])]

    def face_vertex_descendant(self, fkey, key, n=1):
        """Return the n-th vertex after the specified vertex in a specific face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.
        key : int
            The identifier of the vertex.
        n : int, optional
            The index of the vertex descendant.
            Default is 1, meaning the next vertex.

        Returns
        -------
        int
            The identifier of the vertex after the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        i = self.face[fkey].index(key)
        return self.face[fkey][(i + n) % len(self.face[fkey])]

    def face_adjacency_halfedge(self, f1, f2):
        """Find one half-edge over which two faces are adjacent.

        Parameters
        ----------
        f1 : int
            The identifier of the first face.
        f2 : int
            The identifier of the second face.

        Returns
        -------
        tuple[int, int] | None
            The half-edge separating face 1 from face 2,
            or None, if the faces are not adjacent.

        Notes
        -----
        For use in form-finding algorithms, that rely on form-force duality information,
        further checks relating to the orientation of the corresponding are required.

        """
        for u, v in self.face_halfedges(f1):
            if self.halfedge[v][u] == f2:
                return u, v

    def face_adjacency_vertices(self, f1, f2):
        """Find all vertices over which two faces are adjacent.

        Parameters
        ----------
        f1 : int
            The identifier of the first face.
        f2 : int
            The identifier of the second face.

        Returns
        -------
        list[int] | None
            The vertices separating face 1 from face 2,
            or None, if the faces are not adjacent.

        """
        return [vkey for vkey in self.face_vertices(f1) if vkey in self.face_vertices(f2)]

    def is_face_on_boundary(self, key):
        """Verify that a face is on a boundary.

        Parameters
        ----------
        key : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        """
        a = [self.halfedge[v][u] for u, v in self.face_halfedges(key)]
        if None in a:
            return True
        else:
            return False

    face_vertex_after = face_vertex_descendant
    face_vertex_before = face_vertex_ancestor

    def halfedge_after(self, edge):
        """Find the halfedge after the given halfedge in the same face.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.

        Returns
        -------
        tuple[int, int]
            The next halfedge.

        """
        u, v = edge
        face = self.halfedge_face(edge)
        if face is not None:
            w = self.face_vertex_after(face, v)
            return v, w
        nbrs = self.vertex_neighbors(v, ordered=True)
        w = nbrs[0]
        return v, w

    def halfedge_before(self, edge):
        """Find the halfedge before the given halfedge in the same face.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.

        Returns
        -------
        tuple[int, int]
            The previous halfedge.

        """
        u, v = edge
        face = self.halfedge_face(edge)
        if face is not None:
            t = self.face_vertex_before(face, u)
            return t, u
        nbrs = self.vertex_neighbors(u, ordered=True)
        t = nbrs[-1]
        return t, u

    def vertex_edges(self, vertex):
        """Find all edges connected to a given vertex.

        Parameters
        ----------
        vertex : int

        Returns
        -------
        list[tuple[int, int]]

        """
        edges = []
        for nbr in self.vertex_neighbors(vertex):
            if self.has_edge((vertex, nbr)):
                edges.append((vertex, nbr))
            else:
                edges.append((nbr, vertex))
        return edges

    def halfedge_loop_vertices(self, edge):
        """Find all vertices on the same loop as a given halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.
        Returns
        -------
        list[int]
            The vertices on the same loop as the given halfedge.

        """
        loop = self.halfedge_loop(edge)
        return [loop[0][0]] + [edge[1] for edge in loop]

    def halfedge_strip_faces(self, edge):
        """Find all faces on the same strip as a given halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.

        Returns
        -------
        list[int]
            The faces on the same strip as the given halfedge.

        """
        strip = self.halfedge_strip(edge)
        return [self.halfedge_face(edge) for edge in strip]

    # --------------------------------------------------------------------------
    # boundaries
    # --------------------------------------------------------------------------

    def vertices_on_boundary(self):
        """Find the vertices on the longest boundary.

        Returns
        -------
        list[int]
            The vertices of the longest boundary.

        """
        boundaries = self.vertices_on_boundaries()
        return boundaries[0] if boundaries else []

    def edges_on_boundary(self):
        """Find the edges on the longest boundary.

        Returns
        -------
        list[tuple[int, int]]
            The edges of the longest boundary.

        """
        boundaries = self.edges_on_boundaries()
        return boundaries[0] if boundaries else []

    def faces_on_boundary(self):
        """Find the faces on the longest boundary.

        Returns
        -------
        list[int]
            The faces on the longest boundary.

        """
        boundaries = self.faces_on_boundaries()
        return boundaries[0] if boundaries else []

    def vertices_on_boundaries(self):
        """Find the vertices on all boundaries of the mesh.

        Returns
        -------
        list[list[int]]
            A list of vertex keys per boundary.
            The boundary with the most vertices is returned first.

        """
        # all boundary vertices
        vertices_set = set()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, face in iter(nbrs.items()):
                if face is None:
                    vertices_set.add(key)
                    vertices_set.add(nbr)
        vertices_all = list(vertices_set)

        # return an empty list if there are no boundary vertices
        if not vertices_all:
            return []

        # init container for boundary groups
        boundaries = []

        # identify *special* vertices
        # these vertices are non-manifold
        # and should be processed differently
        special = []
        for key in vertices_all:
            count = 0
            for nbr in self.vertex_neighbors(key):
                face = self.halfedge_face((key, nbr))
                if face is None:
                    count += 1
                    if count > 1:
                        if key not in special:
                            special.append(key)

        superspecial = special[:]

        # process the special vertices first
        while special:
            start = special.pop()
            nbrs = []
            # find all neighbors of the current special vertex
            # that are on the mesh boundary
            for nbr in self.vertex_neighbors(start):
                face = self.halfedge_face((start, nbr))
                if face is None:
                    nbrs.append(nbr)
            # for normal mesh vertices
            # there should be only 1 boundary neighbor
            # for special vertices there are more and they all have to be processed
            while nbrs:
                vertex = nbrs.pop()
                vertices = [start, vertex]
                while True:
                    # this is a *super* special case
                    if vertex in superspecial:
                        boundaries.append(vertices)
                        break
                    # find the boundary loop for the current starting halfedge
                    for nbr in self.vertex_neighbors(vertex):
                        if nbr == vertices[-2]:
                            continue
                        face = self.halfedge_face((vertex, nbr))
                        if face is None:
                            vertices.append(nbr)
                            vertex = nbr
                            break
                    if vertex == start:
                        boundaries.append(vertices)
                        break
                # remove any neighbors that might be part of an already identified boundary
                nbrs = [vertex for vertex in nbrs if vertex not in vertices]

        # remove all boundary vertices that were already identified
        vertices_all = [vertex for vertex in vertices_all if all(vertex not in vertices for vertices in boundaries)]

        # process the remaining boundary vertices if any
        if vertices_all:
            key = vertices_all[0]
            while vertices_all:
                vertices = [key]
                start = key
                while True:
                    for nbr in self.vertex_neighbors(key):
                        face = self.halfedge_face((key, nbr))
                        if face is None:
                            vertices.append(nbr)
                            key = nbr
                            break
                    if key == start:
                        boundaries.append(vertices)
                        vertices_all = [x for x in vertices_all if x not in vertices]
                        break
                if vertices_all:
                    key = vertices_all[0]

        # return the boundary groups in order of the length of the group
        return sorted(boundaries, key=lambda vertices: len(vertices), reverse=True)

    def edges_on_boundaries(self):
        """Find the edges on all boundaries of the mesh.

        Returns
        -------
        list[list[tuple[int, int]]]
            A list of edges per boundary.

        """
        vertexgroups = self.vertices_on_boundaries()
        edgegroups = []
        for vertices in vertexgroups:
            edgegroups.append(list(pairwise(vertices)))
        return edgegroups

    def faces_on_boundaries(self):
        """Find the faces on all boundaries of the mesh.

        Returns
        -------
        list[list[int]]
            lists of faces, grouped and sorted per boundary.

        """
        vertexgroups = self.vertices_on_boundaries()
        facegroups = []
        for vertices in vertexgroups:
            temp = [self.halfedge_face((v, u)) for u, v in pairwise(vertices)]
            faces = []
            for face in temp:
                if face is None:
                    continue
                if face not in faces and all(face not in group for group in facegroups):
                    faces.append(face)
            if faces:
                facegroups.append(faces)
        return facegroups

    # --------------------------------------------------------------------------
    # matrices
    # --------------------------------------------------------------------------

    def adjacency_matrix(self, rtype="array"):
        """Compute the adjacency matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The adjacency matrix.

        """
        from compas.topology import adjacency_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return adjacency_matrix(adjacency, rtype=rtype)

    def connectivity_matrix(self, rtype="array"):
        """Compute the connectivity matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The connectivity matrix.

        """
        from compas.topology import connectivity_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return connectivity_matrix(adjacency, rtype=rtype)

    def degree_matrix(self, rtype="array"):
        """Compute the degree matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The degree matrix.

        """
        from compas.topology import degree_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return degree_matrix(adjacency, rtype=rtype)

    def face_matrix(self, rtype="array"):
        r"""Compute the face matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The face matrix.

        Notes
        -----
        The face matrix represents the relationship between faces and vertices.
        Each row of the matrix represents a face. Each column represents a vertex.
        The matrix is filled with zeros except where a relationship between a vertex
        and a face exist.

        .. math::

            F_{ij} =
            \begin{cases}
                1 & \text{if vertex j is part of face i} \\
                0 & \text{otherwise}
            \end{cases}

        The face matrix can for example be used to compute the centroids of all
        faces of a mesh.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_polyhedron(6)
        >>> F = mesh.face_matrix()
        >>> type(F)
        <class 'numpy.ndarray'>

        >>> from numpy import allclose
        >>> xyz = asarray(mesh.vertices_attributes('xyz'))
        >>> F = mesh.face_matrix(mesh, rtype='csr')
        >>> c1 = F.dot(xyz) / F.sum(axis=1)
        >>> c2 = [mesh.face_centroid(fkey) for fkey in mesh.faces()]
        >>> allclose(c1, c2)
        True

        """
        from compas.topology import face_matrix

        vertex_index = self.vertex_index()
        faces = [[vertex_index[vertex] for vertex in self.face_vertices(face)] for face in self.faces()]
        return face_matrix(faces, rtype=rtype)

    def laplacian_matrix(self, rtype="array"):
        r"""Compute the Laplacian matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The Laplacian matrix.

        Notes
        -----
        The :math:`n \times n` uniform Laplacian matrix :math:`\mathbf{L}` of a mesh
        with vertices :math:`\mathbf{V}` and edges :math:`\mathbf{E}` is defined as
        follows [1]_

        .. math::

            \mathbf{L}_{ij} =
            \begin{cases}
                -1               & i = j \\
                \frac{1}{deg(i)} & (i, j) \in \mathbf{E} \\
                0                & \text{otherwise}
            \end{cases}

        with :math:`deg(i)` the degree of vertex :math:`i`.

        Therefore, the uniform Laplacian of a vertex :math:`\mathbf{v}_{i}` points to
        the centroid of its neighboring vertices.

        References
        ----------
        .. [1] Nealen A., Igarashi T., Sorkine O. and Alexa M.
            `Laplacian Mesh Optimization <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-optimization/lmo.pdf>`_.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_polyhedron(6)
        >>> L = mesh.laplacian_matrix(mesh, rtype='array')
        >>> type(L)
        <class 'numpy.ndarray'>

        >>> xyz = asarray(mesh.vertices_attributes('xyz'))
        >>> L = mesh.laplacian_matrix(mesh)
        >>> d = L.dot(xyz)

        """
        from compas.topology import laplacian_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return laplacian_matrix(adjacency, rtype=rtype)
