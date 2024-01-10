from setuptools import setup
import versioneer

setup(name='gcode_helpers',
      # version='0.1.5',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='`gcode_helpers`-- collection of helper functions for parsing raw gcode',
      url='https://github.com/rtellez700/gcode_helpers',
      author='Rodrigo Telles',
      author_email='rtelles@g.harvard.edu',
      license='MIT',
    #   packages=[],
      zip_safe=False)