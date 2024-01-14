from setuptools import setup
setup(
    name='knowl_apidocs',
    version='0.2.3',
    url="https://github.com/knowl-doc/APIDocs",
    entry_points={
        'console_scripts': [
            'knowl_apidocs = knowl_apidocs.apidocs:main'
        ]
    },
)