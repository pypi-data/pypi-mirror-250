from setuptools import setup, find_packages

# read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
  long_description = f.read()
  
setup(
  name='futuresio',
  version='0.1.1',
  packages=find_packages(),
  description="Abstract classes defination for I/O operations, those abstract classes follows the Rust's I/O related trait definations.",
  long_description=long_description,
  long_description_content_type='text/markdown',
  license='MIT/Apache-2.0',
  url="http://github.com/al8n/pyo3-io",
  author='Al Liu',
  author_email='scygliu1@gmail.com',
)
