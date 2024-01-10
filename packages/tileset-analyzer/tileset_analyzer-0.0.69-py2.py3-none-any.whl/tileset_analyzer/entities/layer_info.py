import numbers
import math


class LayerInfo:
    def __init__(self, name: str, zoom_level: str):
        self.name = name
        self.count = 0
        self.attributes = set()
        self.attributes_sample_values = {}
        self.attributes_types = {}
        self.attributes_numeric_domain = {}
        self.zoom_level = zoom_level
        self.geometry_types = set()

    def add_feature(self, attributes: dict, geometry_type: str):
        self.count += 1

        # add geometry type
        if geometry_type not in self.geometry_types:
            self.geometry_types.add(geometry_type)

        for key, value in attributes.items():
            if key not in self.attributes:
                self.attributes.add(key)
                self.attributes_sample_values[key] = set()
                self.attributes_types[key] = set()

            # populate attribute value
            attr_values: set = self.attributes_sample_values[key]
            if len(attr_values) < 100:
                if value not in attr_values:
                    attr_values.add(value)

            # populate attribute type
            attr_types: set = self.attributes_types[key]
            attr_type = type(value).__name__
            if attr_type not in attr_types:
                attr_types.add(attr_type)

            # get attribute numeric domain
            if isinstance(value, numbers.Number):
                if key not in self.attributes_numeric_domain:
                    self.attributes_numeric_domain[key] = [math.inf, -math.inf]

                attr_domain = self.attributes_numeric_domain[key]
                if value < attr_domain[0]:
                    attr_domain[0] = value
                if value > attr_domain[1]:
                    attr_domain[1] = value
