from __future__ import absolute_import, print_function, unicode_literals
from json import schema
from jsonspec.validators.exceptions import ValidationError
import os

here = os.path.dirname(os.path.abspath(__file__))

dataset = [
    ('basic.json', {
        'firstName': 'John',
        'lastName': 'Noone',
        'age': 33,
    }),
    ('simple.json', [{
        'id': 1,
        'name': 'A green door',
        'price': 12.50,
        'tags': ['home', 'green']
    }]),
]

for filename, data in dataset:
    with open(os.path.join(here, filename)) as file:
        print('validate {}'.format(filename))

        validator = schema.load(file)
        try:
            validator.validate(data)
            print('all fine')
        except ValidationError as error:
            print(error)
