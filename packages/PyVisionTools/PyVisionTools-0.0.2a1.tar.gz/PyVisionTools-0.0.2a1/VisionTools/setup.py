import setuptools


with open('VisionTools/README.md', 'r') as fhandle:
    long_description = fhandle.read()


setuptools.setup(
    name='PyVisionTools',
    version='0.0.2a1',
    author='varenikGD',
    author_email='arugula_baklava.0o@icloud.com',
    description='A collection of tools for image processing',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/varenikGD/PyVisionTools',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      install_requires=[
          'Pillow',
      ],
      python_requires='>=3.6',
  )