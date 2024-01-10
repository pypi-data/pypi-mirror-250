"""Define the package metadata and register plugin with flake8."""

from setuptools import setup

setup(
    name='self-documenting-f-string',
    version='0.1',
    description='flake8 plugin to run pycodecheck but ignore their incorrect self-documenting f-string errors in Python 3.12',
    author='Brent Wilkins',
    author_email='brent@wilkins.in',
    url='https://github.com/brentwilkins/self-documenting-f-string',
    packages=['self_documenting_f_string'],
    entry_points={
        'flake8.extension': [
            'E = self_documenting_f_string.f_string_rule:CustomChecker',
        ],
    },
)
