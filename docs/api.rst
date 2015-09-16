.. _api:

API Reference
=============

FeatureSystem
-------------

.. autofunction:: features.make_features

.. autoclass:: features.FeatureSystem
    :members:
        __call__, __getitem__, __iter__, __len__, __contains__,
        atoms,
        join, meet,
        upset_union, downset_union,
        graphviz


FeatureSet
----------
.. autoclass:: features.bases.FeatureSet
    :members:
        atoms,
        upper_neighbors, lower_neighbors,
        upset, downset,
        subsumes, implies,
        properly_subsumes, properly_implies,
        intersection, union,
        incompatible_with, complement_of, subcontrary_with, orthogonal_to


Config
------

.. autofunction:: features.add_config

.. autoclass:: features.Config
    :members:
