from setuptools import setup
setup(
    name='knowl_apidocs',
    version='0.1.0',
    url="https://github.com/knowl-doc/APIDocs",
    entry_points={
        'console_scripts': [
            'knowl_apidocs = knowl_apidocs.apidocs:main'
        ]
    },
)