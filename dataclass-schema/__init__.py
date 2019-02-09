from dataclasses import dataclass, fields, Field, is_dataclass
from typing import List

_schemas = {}

_classes = []


def schematize(cls):
    _classes.append(cls)
    return cls


@dataclass
@schematize
class InnerClass:
    prop_c: int


@dataclass
@schematize
class OuterClass:
    prop_a: int
    prop_b: InnerClass
    prop_f: List[InnerClass]


TYPE_FIELDS_SCHEMA = {
    int: lambda x: {
        "type": "integer"
    },
    List: lambda x: {
        "type": "array",
        "item": {
            # TODO:
            "ref": "Nested object"
        } if x.__args__[0] in _classes else x.__args__[0]
    }
}


def parse_field(field: Field):
    if is_dataclass(field.type):
        yield {
            field.name: {
                "type": "object",
                "ref": field.type.__name__
            }
        }
        # yield from parse_class(field.type)

    else:
        for key, value in TYPE_FIELDS_SCHEMA.items():
            print(field)
            print(field.type)
            if issubclass(field.type, key):
                yield {
                    field.name: value(field.type)
                }


def parse_class(cls):
    for field in fields(cls):
        for f in parse_field(field):
            yield (
                cls.__name__, f
            )


def generate_schemas():
    a = [s for cls in _classes for s in parse_class(cls)]
    print(a)

    for t in a:
        _schemas.setdefault(t[0], {}).update(t[1])


def get_schemas():
    return _schemas


generate_schemas()

if __name__ == '__main__':
    # for key, group in itertools.groupby(a, key=lambda x: x.keys()):
    #     for k in key:
    #         for g in group:
    #             schemas.setdefault(k, {}).update(g[k])

    print(get_schemas())
