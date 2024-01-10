from setuptools import setup, find_packages

setup(
    name='arafkhan_hello',
    version='0.4',
    packages=['arafkhan_hello'],
    url='',
    license='',
    author='Araf',
    author_email='arafkhan565@gmail.com',
    description='Simple Hello world package',
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "arafkhan-hello = arafkhan_hello:hello",
        ],
    },
)
