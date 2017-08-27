from setuptools import setup, find_packages

setup(name='bliztop',
      version='0.1',
      description='Blizzard senior linux admin coding challenge',
      url='http://github.com/computermax11/bliztop.git',
      author='Max Schulberg',
      author_email='computermax11@gmail.com',
      install_requires=[
          'psutil',
          'statistics',
      ],  
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['bliztop = bliztop.__main__:main'],
      },
      )
