# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geodantic']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'geodantic',
    'version': '0.3.0',
    'description': 'GeoJSON parsing and validation using Pydantic',
    'long_description': '# geodantic\n\n[![pypi](https://img.shields.io/pypi/v/geodantic.svg)](https://pypi.python.org/pypi/geodantic)\n[![versions](https://img.shields.io/pypi/pyversions/geodantic.svg)](https://github.com/alexandermalyga/geodantic)\n\nLightweight, type-safe and spec-conforming [GeoJSON](https://datatracker.ietf.org/doc/html/rfc7946) parsing and validation using Pydantic.\n\n## Installation\n\n```\npip install geodantic\n```\n\n## Examples\n\nParse and validate GeoJSON features with custom properties:\n\n```python\nimport pydantic\nfrom geodantic import Feature, Point\n\n# Use your own properties Pydantic models\n@pydantic.dataclasses.dataclass\nclass MyProperties:\n    foo: str\n\ndata = {\n    "type": "Feature",\n    "geometry": {"type": "Point", "coordinates": [1, 2]},\n    "properties": {"foo": "abc"},\n}\n\n# Parse and validate data into spec-conforming objects\nparsed = Feature[Point, MyProperties](**data)\n"""\nFeature[Point, MyProperties](\n    type=<GeoJSONObjectType.FEATURE: \'Feature\'>, \n    bbox=None, \n    geometry=Point(\n        type=<GeoJSONObjectType.POINT: \'Point\'>, \n        bbox=None, \n        coordinates=(1.0, 2.0)\n    ), \n    properties=MyProperties(foo=\'abc\'), \n    id=None\n)\n"""\n\n# Dump back into JSON using standard Pydantic methods\nparsed.model_dump_json(exclude_unset=True, indent=2)\n"""\n{\n  "type": "Feature",\n  "geometry": {\n    "type": "Point",\n    "coordinates": [\n      1.0,\n      2.0\n    ]\n  },\n  "properties": {\n    "foo": "abc"\n  }\n}\n"""\n```\n\nParse objects of arbitrary types:\n\n```python\nfrom geodantic import GeometryCollection\n\ndata = {\n    "type": "GeometryCollection",\n    "geometries": [\n        {\n            "type": "Polygon",\n            "coordinates": [[[1, 2], [3, 4], [5, 6], [1, 2]]],\n            "bbox": [1, 2, 3, 4],\n        },\n        {\n            "type": "GeometryCollection",\n            "geometries": [{"type": "Point", "coordinates": [1, 2]}],\n        },\n    ],\n}\n\n# Parse any geometry type\nparsed = GeometryCollection(**data)\n"""\nGeometryCollection(\n    type=<GeoJSONObjectType.GEOMETRY_COLLECTION: \'GeometryCollection\'>, \n    bbox=None, \n    geometries=[\n        Polygon(\n            type=<GeoJSONObjectType.POLYGON: \'Polygon\'>, \n            bbox=(1.0, 2.0, 3.0, 4.0), \n            coordinates=[[(1.0, 2.0), (3.0, 4.0), (5.0, 6.0), (1.0, 2.0)]]\n        ), \n        GeometryCollection(\n            type=<GeoJSONObjectType.GEOMETRY_COLLECTION: \'GeometryCollection\'>, \n            bbox=None, \n            geometries=[\n                Point(\n                    type=<GeoJSONObjectType.POINT: \'Point\'>, \n                    bbox=None, \n                    coordinates=(1.0, 2.0)\n                )\n            ]\n        )\n    ]\n)\n"""\n```\n\n## Contributing\n\nSet up the project using [Poetry](https://python-poetry.org/):\n\n```\npoetry install\n```\n\nFormat the code:\n\n```\nmake lint\n```\n\nRun tests:\n\n```\nmake test\n```\n\nCheck for typing and format issues:\n\n```\nmake check\n```\n',
    'author': 'Alexander Malyga',
    'author_email': 'alexander@malyga.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alexandermalyga/geodantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
