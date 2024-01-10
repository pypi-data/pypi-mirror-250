from setuptools import setup

version = '0.0.1'

with open('README.md', encoding='utf-8') as f:
    description = f.read()

setup(
    name='entity_auth',
    version=version,

    author='gangstand',
    author_email='ganggstand@gmail.ru',

    description=(
        u'A FastAPI extension that provides support for JWT authentication (secure, easy to use, and lightweight).'
    ),
    long_description=description,
    long_description_content_type='text/markdown',

    url='https://github.com/gangstand/entity_auth',

    license='License :: OSI Approved :: MIT License',

    packages=['entity_auth'],
    install_requires=['pyjwt', 'fastapi', 'mypy'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ]
)
