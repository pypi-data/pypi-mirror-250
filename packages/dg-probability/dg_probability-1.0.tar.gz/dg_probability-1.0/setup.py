from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='dg_probability',
      version='1.0',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['dg_probability'],
      author="Shamir Alavi",
      author_email="dg1223.dev@gmail.com",
      zip_safe=False)
