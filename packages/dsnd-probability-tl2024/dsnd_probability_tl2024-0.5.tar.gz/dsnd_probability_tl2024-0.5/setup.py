from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setup(name='dsnd_probability_tl2024',
      version='0.5',
      description='Gaussian Binomial distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['dsnd_probability_tl2024'],
      author='Tony Lockhart',
      author_email='Tony.Lockhart@ymail.com',
      zip_safe=False)