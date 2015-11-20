.. _api:

API Reference
=============

.. autofunction:: features.add_config

.. autofunction:: features.make_features


FeatureSystem
-------------

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

.. autoclass:: features.Config
    :members:
