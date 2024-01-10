from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
readme = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='tice',
    version='2.1',
    description='Tic-Tac-Toe in Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/tic-tac-toe-in-python',
    author='tice',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='tic-tac-toe, ttt, ai, multiplayer, min, max, minmax, minimax',
    include_package_data=True,
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)