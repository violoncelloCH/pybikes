import json
from pkg_resources import resource_string

import pytest

from pybikes import BikeShareSystem, BikeShareStation
from pybikes.utils import filter_bounds, Bounded

barcelona = [
    BikeShareStation(latitude=41.38530363280023, longitude=2.1537750659833534),
    BikeShareStation(latitude=41.38670644238084, longitude=2.14627128),
]

girona = [
    BikeShareStation(latitude=41.97290243618622, longitude=2.812822876238897),
]

mordor = [
    BikeShareStation(latitude=-100, longitude=3000),
    BikeShareStation(latitude=0, longitude=0),
]

morpork = [
    BikeShareStation(latitude=-180, longitude=-90),
    BikeShareStation(latitude=180, longitude=90),
]

shape = json.loads(resource_string('tests.fixtures', 'shape.json'))
multipolygon = json.loads(resource_string('tests.fixtures', 'multipolygon.json'))
hole = json.loads(resource_string('tests.fixtures', 'hole.json'))

filter_bounds_cases = [
    (
        "A bbox filter of barcelona displays only stations in Barcelona",
        barcelona + girona + mordor + morpork,
        barcelona,
        None,
        [[41.429655489542995, 2.265798843028506], [41.324098007178094, 2.060483133624132]]
    ),
    (
        "A geojson shape filter displays only stations within the filter",
        barcelona + girona + mordor + morpork,
        barcelona + girona,
        None,
        shape
    ),
    (
        "A bbox filter of points using a getter display only points within bbox",
        [
            {'lat': 41.3853036328, 'lng': 2.1537750659833534},
            {'lat': 31.3853036328, 'lng': 1.1537750659833534},
        ],
        [
            {'lat': 41.3853036328, 'lng': 2.1537750659833534},
        ],
        lambda thing: (thing['lat'], thing['lng']),
        [[41.429655489542995, 2.265798843028506], [41.324098007178094, 2.060483133624132]],
    ),
    (
        "A shape filter of points using a getter display only points within bbox",
        [
            {'lat': 41.3853036328, 'lng': 2.1537750659833534},
            {'lat': 31.3853036328, 'lng': 1.1537750659833534},
        ],
        [
            {'lat': 41.3853036328, 'lng': 2.1537750659833534},
        ],
        lambda thing: (thing['lat'], thing['lng']),
        shape
    ),
    (
        "A bbox filter of pairs display only points within bbox",
        [
            (41.3853036328, 2.1537750659833534),
            (31.3853036328, 1.1537750659833534),
        ],
        [
            (41.3853036328, 2.1537750659833534),
        ],
        None,
        [[41.429655489542995, 2.265798843028506], [41.324098007178094, 2.060483133624132]],
    ),
    (
        "A shape filter of pairs display only points within bbox",
        [
            (41.3853036328, 2.1537750659833534),
            (31.3853036328, 1.1537750659833534),
        ],
        [
            (41.3853036328, 2.1537750659833534),
        ],
        None,
        shape
    ),
    (
        "A filter with a split multipolygon displays only stations within",
        [
            (40.06787253110281, -1.2728061635069423),
            (39.45257232150425, -0.11859136593309927),
            (39.46613316471084, -0.37452595148192813),
        ],
        [
            (40.06787253110281, -1.2728061635069423),
            (39.46613316471084, -0.37452595148192813),
        ],
        None,
        multipolygon
    ),
    (
        "A polygon with a hole displays only stations within the filter",
        [
            (0, 0),
            (51.5, 0),
        ],
        [
            (51.5, 0),
        ],
        None,
        hole
    ),
]

@pytest.mark.parametrize("msg, data, expected, getter, bounds", filter_bounds_cases)
def test_filter_bounds(msg, data, expected, getter, bounds):
    assert expected == list(filter_bounds(data, getter, bounds)), msg


class TestBounded:

    class BoundsSystem(Bounded, BikeShareSystem):
        pass

    def test_with_no_bounds(self):
        tag = 'foo'
        meta = {'name': 'Foo', 'system': 'Foo'}
        bbox = None
        foo = TestBounded.BoundsSystem(tag, meta, bounds=bbox)
        foo.stations = [
            (41.3853036328, 2.1537750659833534),
            (31.3853036328, 1.1537750659833534),
        ]
        assert [
            (41.3853036328, 2.1537750659833534),
            (31.3853036328, 1.1537750659833534),
        ] == foo.stations


    def test_with_bounds(self):
        tag = 'foo'
        meta = {'name': 'Foo', 'system': 'Foo'}
        bbox = [[41.429655489542995, 2.265798843028506], [41.324098007178094, 2.060483133624132]]
        foo = TestBounded.BoundsSystem(tag, meta, bounds=bbox)
        foo.stations = [
            (41.3853036328, 2.1537750659833534),
            (31.3853036328, 1.1537750659833534),
        ]
        assert [
            (41.3853036328, 2.1537750659833534),
        ] == foo.stations
