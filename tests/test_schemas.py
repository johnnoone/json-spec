#!/usr/bin/env python

"""
    tests_validators
    ~~~~~~~~~~~~~~~~

"""

import unittest
from jsontools.schema import loads
from jsontools.exceptions import ValidationError


class TestSchema(unittest.TestCase):
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

    def test_four(self):
        data = {
            "/": {
                "storage": {
                    "type": "disk",
                    "device": "/dev/sda1"
                },
                "fstype": "btrfs",
                "readonly": True
            },
            "/var": {
                "storage": {
                    "type": "disk",
                    "label": "8f3ba6f4-5c70-46ec-83af-0d5434953e5f"
                },
                "fstype": "ext4",
                "options": [ "nosuid" ]
            },
            "/tmp": {
                "storage": {
                    "type": "tmpfs",
                    "sizeInMB": 64
                }
            },
            "/var/www": {
                "storage": {
                    "type": "nfs",
                    "server": "my.nfs.server",
                    "remotePath": "/exports/mypath"
                }
            }
        }

        base_schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "/": { "$ref": "http://some.site.somewhere/entry-schema#" }
            },
            "patternProperties": {
                "^(/[^/]+)+$": { "$ref": "http://some.site.somewhere/entry-schema#" }
            },
            "additionalProperties": False,
            "required": [ "/" ]
        }

        entry_schema = {
            "id": "http://some.site.somewhere/entry-schema#",
            "$schema": "http://json-schema.org/draft-04/schema#",
            "description": "schema for an fstab entry",
            "type": "object",
            "required": [ "storage" ],
            "properties": {
                "storage": {
                    "type": "object",
                    "oneOf": [
                        { "$ref": "#/definitions/diskDevice" },
                        { "$ref": "#/definitions/diskUUID" },
                        { "$ref": "#/definitions/nfs" },
                        { "$ref": "#/definitions/tmpfs" }
                    ]
                },
                "fstype": {
                    "enum": [ "ext3", "ext4", "btrfs" ]
                },
                "options": {
                    "type": "array",
                    "minItems": 1,
                    "items": { "type": "string" },
                    "uniqueItems": True
                },
                "readonly": { "type": "boolean" }
            },
            "definitions": {
                "diskDevice": {
                    "properties": {
                        "type": { "enum": [ "disk" ] },
                        "device": {
                            "type": "string",
                            "pattern": "^/dev/[^/]+(/[^/]+)*$"
                        }
                    },
                    "required": [ "type", "device" ],
                    "additionalProperties": False
                },
                "diskUUID": {
                    "properties": {
                        "type": { "enum": [ "disk" ] },
                        "label": {
                            "type": "string",
                            "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
                        }
                    },
                    "required": [ "type", "label" ],
                    "additionalProperties": False
                },
                "nfs": {
                    "properties": {
                        "type": { "enum": [ "nfs" ] },
                        "remotePath": {
                            "type": "string",
                            "pattern": "^(/[^/]+)+$"
                        },
                        "server": {
                            "type": "string",
                            "oneOf": [
                                { "format": "host-name" },
                                { "format": "ipv4" },
                                { "format": "ipv6" }
                            ]
                        }
                    },
                    "required": [ "type", "server", "remotePath" ],
                    "additionalProperties": False
                },
                "tmpfs": {
                    "properties": {
                        "type": { "enum": [ "tmpfs" ] },
                        "sizeInMB": {
                            "type": "integer",
                            "minimum": 16,
                            "maximum": 512
                        }
                    },
                    "required": [ "type", "sizeInMB" ],
                    "additionalProperties": False
                }
            }
        }
        validator = loads(base_schema, loader={
            'http://some.site.somewhere/entry-schema#': entry_schema
        })
        validator.validate(data)

if __name__ == '__main__':
    unittest.main()
