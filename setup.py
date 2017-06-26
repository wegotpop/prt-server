from setuptools import setup, find_packages

setup(name='prt',
      description='PRT reference server-side implementation',
      long_description=('PRT (POP Rich Text) is a safe, small and strict rich '
                        'text serialisation protocol which can be used for '
                        'example in server - client communications. More info '
                        'on the protocol: https://github.com/wegotpop/prt'),
      version='1.0.0',
      url='https://github.com/wegotpop/prt-server',
      author='We Got POP Ltd.',
      author_email='devops@wegotpop.com',
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7'],
      packages=find_packages(where='src/python2'),
      package_dir={'': 'src/python2'},
      python_requires='>=2.7',
      install_requires=['enum34>=1.1.6',
                        'lxml>=3.8.0'])
