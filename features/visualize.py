# visualize.py - generate graphviz dot source of feature lattice

import graphviz

__all__ = ['featuresystem', 'render_all']

DIRECTORY = 'graphs'

MAXIMAL_LABEL = False

TOPDOWN = False

NAME_GETTERS = [lambda f: 'f%d' % f.index, lambda f: repr(f)]

LABEL_GETTERS = [
    lambda f: f.string.replace('-', '&minus;'),
    lambda f: f. string_maximal.replace('-', '&minus;')
]

NEIGHBORS_GETTERS = [lambda f: f.lower_neighbors, lambda f: f.upper_neighbors]


def featuresystem(fs, highlight, maximal_label, topdown,
                  filename, directory, render, view, **kwargs):
    if maximal_label is None:
        maximal_label = MAXIMAL_LABEL

    if topdown is None:
        topdown = TOPDOWN

    name = fs.key if fs.key is not None else '%#x' % id(fs)

    if filename is None:
        filename = 'fs-%s%s.gv' % (name, '-max' if maximal_label else '')

    dot = graphviz.Digraph(name=name,
                           comment=repr(fs),
                           filename=filename,
                           directory=directory,
                           graph_attr={'margin': '0'},
                           edge_attr={'arrowtail': 'none', 'penwidth': '.5'},
                           **kwargs)

    if highlight is not None:
        def node_format(f, dw=set(highlight.downset), up=set(highlight.upset)):
            if f in dw:
                return (('style', 'filled'), ('color', 'gray60'))
            elif f in up:
                return (('style', 'filled'), ('color', 'gray80'))
            elif f is highlight:
                return (('style', 'filled'), ('color', 'gray20'))
    else:
        node_format = lambda f: None  # noqa: E731

    node_name = NAME_GETTERS[0]

    node_label = LABEL_GETTERS[bool(maximal_label)]

    node_neighbors = NEIGHBORS_GETTERS[bool(topdown)]

    if not topdown:
        dot.edge_attr.update(dir='back')

    sortkey = lambda f: f.index  # noqa: E731

    for f in fs._featuresets:
        name = node_name(f)
        dot.node(name, node_label(f), node_format(f))
        dot.edges((name, node_name(n))
                  for n in sorted(node_neighbors(f), key=sortkey))

    if render or view:
        dot.render(view=view)  # pragma: no cover
    return dot


def render_all(maximal_label=MAXIMAL_LABEL, topdown=TOPDOWN,
               directory=DIRECTORY, format=None):  # pragma: no cover
    from features.systems import FeatureSystem
    from features.meta import Config

    for conf in Config:
        fs = FeatureSystem(conf)
        dot = fs.graphviz(maximal_label=maximal_label, topdown=topdown,
                          directory=directory, format=format)
        dot.render()
