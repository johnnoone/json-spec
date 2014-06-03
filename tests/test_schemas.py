#!/usr/bin/env python

"""
    tests_validators
    ~~~~~~~~~~~~~~~~

"""

import unittest
from jsontools.schema import loads
from jsontools.exceptions import ValidationError


class TestNumber(unittest.TestCase):
    def test_first(self):
        """examples taken from
        http://spacetelescope.github.io/understanding-json-schema/about.html#about"""

        data1 = {
          "name": "George Washington",
          "birthday": "February 22, 1732",
          "address": "Mount Vernon, Virginia, United States"
        }

        data2 = {
          "first_name": "George",
          "last_name": "Washington",
          "birthday": "1732-02-22",
          "address": {
            "street_address": "3200 Mount Vernon Memorial Highway",
            "city": "Mount Vernon",
            "state": "Virginia",
            "country": "United States"
          }
        }

        schema = {
          "type": "object",
          "properties": {
            "first_name": { "type": "string" },
            "last_name": { "type": "string" },
            "birthday": { "type": "string", "format": "date-time" },
            "address": {
              "type": "object",
              "properties": {
                "street_address": { "type": "string" },
                "city": { "type": "string" },
                "state": { "type": "string" },
                "country": { "type" : "string" }
              }
            }
          }
        }
        validator = loads(schema)
        with self.assertRaises(ValidationError):
            validator.validate(data1)
        validator.validate(data2)

    def test_second(self):
        """examples taken from
        http://spacetelescope.github.io/understanding-json-schema/structuring.html#structuring"""
        schema = {
          "$schema": "http://json-schema.org/draft-04/schema#",

          "definitions": {
            "address": {
              "type": "object",
              "properties": {
                "street_address": { "type": "string" },
                "city":           { "type": "string" },
                "state":          { "type": "string" }
              },
              "required": ["street_address", "city", "state"]
            }
          },

          "type": "object",

          "properties": {
            "billing_address": { "$ref": "#/definitions/address" },
            "shipping_address": { "$ref": "#/definitions/address" }
          }
        }
        data = {
          "shipping_address": {
            "street_address": "1600 Pennsylvania Avenue NW",
            "city": "Washington",
            "state": "DC"
          },
          "billing_address": {
            "street_address": "1st Street SE",
            "city": "Washington",
            "state": "DC"
          }
        }
        validator = loads(schema)
        validator.validate(data)

    def test_three(self):
        schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",

            "definitions": {
                "address": {
                    "type": "object",
                    "properties": {
                        "street_address": { "type": "string" },
                        "city":           { "type": "string" },
                        "state":          { "type": "string" }
                    },
                    "required": ["street_address", "city", "state"]
                }
            },

            "type": "object",

            "properties": {
                "billing_address": { "$ref": "#/definitions/address" },
                "shipping_address": {
                    "allOf": [
                        {
                            "$ref": "#/definitions/address"
                        },
                        {
                            "properties": {
                                "type": {
                                    "enum": ["residential", "business"]
                                }
                            },
                            "required": ["type"]
                        }
                    ]
                }
            }
        }

        data1 = {
          "shipping_address": {
            "street_address": "1600 Pennsylvania Avenue NW",
            "city": "Washington",
            "state": "DC"
          }
        }

        data2 = {
          "shipping_address": {
            "street_address": "1600 Pennsylvania Avenue NW",
            "city": "Washington",
            "state": "DC",
            "type": "business"
          }
        }
        validator = loads(schema)
        with self.assertRaises(ValidationError):
            validator.validate(data1)
        validator.validate(data2)

if __name__ == '__main__':
    unittest.main()
