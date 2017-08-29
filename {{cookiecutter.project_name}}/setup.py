#!/usr/bin/python
import setuptools

requires = [
]

setuptools.setup(
    name='{{cookiecutter.module_name}}',
    version='0.0.1',
    description='{{cookiecutter.description}}',
    author='{{cookiecutter.author}}',
    author_email='{{cookiecutter.author_email}}',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        'Development Status :: 1 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: No Input/Output (Daemon)',
    ],
    entry_points={
        'console_scripts': [
            '{{cookiecutter.module_name}}-api = {{cookiecutter.module_name}}.cmd.api:main',
            '{{cookiecutter.module_name}}-manage = {{cookiecutter.module_name}}.cmd.manage:main',
        ]
    },
    py_modules=[],
)
