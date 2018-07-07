from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

setup(name='leauge_of_legends_api',
      version='0.2.3',
      description="A python module for the Leauge of Legends Api which also save's the response to a"
                  " Database with SQLAlchemy",
      long_description=long_description,
      url='https://github.com/Lkgsr/Leauge_of_Legends_api',
      author='Lukas Mahr',
      author_email='mahrlukas2018@gmail.com',
      license='MIT',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords=['leaugoflegends', 'lol', 'LeaugeOfLegends'],
      package_dir={'': 'src'},
      install_requires=['requests', 'sqlalchemy'],
      packages=['', 'Api'],
      zip_safe=False)
