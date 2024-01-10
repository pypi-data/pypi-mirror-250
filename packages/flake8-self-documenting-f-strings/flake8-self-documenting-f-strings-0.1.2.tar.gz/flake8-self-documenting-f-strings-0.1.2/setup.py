"""Define the package metadata and register plugin with flake8."""

from setuptools import setup

setup(
    name='flake8-self-documenting-f-strings',
    version='0.1.2',
    description='flake8 plugin to run pycodecheck but ignore their incorrect self-documenting f-string errors in Python 3.12',
    author='Brent Wilkins',
    author_email='brent@wilkins.in',
    url='https://github.com/brentwilkins/self-documenting-f-string',
    packages=['self_documenting_f_strings'],
    entry_points={
        'flake8.extension': [
            'E = self_documenting_f_strings:FStringChecker',
        ],
    },
)
