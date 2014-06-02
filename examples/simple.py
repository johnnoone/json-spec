from __future__ import absolute_import, print_function, unicode_literals
from jsontools import schema

data = {
    "id": 1,
    "name": "A green door",
    "price": 12.50,
    "tags": ["home", "green"]
}


with open('simple.json') as file:
    validator = load(file)

report = validator.validate(data)
print(report.status)
print(report.errors)
