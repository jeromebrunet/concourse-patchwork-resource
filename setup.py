from setuptools import setup

setup(name='pwresource',
      version='0.1',
      description='Concourse patchwork resource',
      url='http://gitlab.com/jbrunet/pw-resource',
      author='Jerome Brunet',
      author_email='jbrunet@baylibre.com',
      license='MIT',
      packages=['pwresource'],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['check=pwresource.concourse:check',
                              'out=pwresource.concourse:output',
                              'in=pwresource.concourse:input']
      },
      install_requires = [
          'requests'
      ]
)
