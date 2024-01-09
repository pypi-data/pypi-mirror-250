from setuptools import setup

# Read deps
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ivette',
    version='0.4.0',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    py_modules=['run_ivette', 'ivette', 'ivette.file_io_module', 'ivette.IO_module', 'ivette.load_module',
                'ivette.run_module', 'ivette.supabase_module', 'ivette.types', 'ivette.utils', 'ivette.decorators'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ivette=run_ivette:main',
        ],
    },
)
