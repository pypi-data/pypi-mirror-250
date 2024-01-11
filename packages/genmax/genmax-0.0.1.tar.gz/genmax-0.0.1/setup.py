from setuptools import setup, find_packages

setup(
    name='genmax',
    version='0.0.1',
    author='Raza Balbale',
    description='A simple code generation tool.',
    url='https://https://github.com/razaibi/genmax/',
    project_urls={
        'Documentation': 'https://github.com/razaibi/genmax/README.md',
        'Source': 'https://github.com/razaibi/genmax',
        'Tracker': 'https://github.com/razaibi/genmax/',
    },
    keywords='cli code generator automation',
    packages=find_packages(),
    install_requires=[
        "PyYAML==6.0",
        "Jinja2==3.1.2",
        "pluralizer==1.2.0",
        "case-switcher==1.3.13",
        "typer==0.9.0"
    ],
    license='Apache 2.0',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gmx=gmx.main:app',
        ],
    },
)
