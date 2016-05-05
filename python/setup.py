from setuptools import setup, find_packages

setup(
        name="auto-tagger",
        version="0.1",
        entry_points={
            'console_scripts':[
                'at-linear-regression = autotagger.scripts:linear_regression'
            ]
        }
)
