from setuptools import setup, find_packages
from pathlib import Path

setup(
  name='meu_primeiro_pacote',
  version=1.0,
  description='Este pacote foi criado como exemplo na aula',
  long_description=Path('README.md').read_text(),
  author='Saulo Gil',
  author_email='saulosgil@hotmail.com',
  keywords=['primeiro', 'pacote', 'criar'],
  packages=find_packages()
  )
