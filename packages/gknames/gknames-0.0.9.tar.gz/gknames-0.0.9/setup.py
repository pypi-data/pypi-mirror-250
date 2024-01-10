from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/gknames/__version__.py").read())

def readme():
    with open(moduleDirectory + '/README.md') as f:
        return f.read()

setup(
    name="gknames",
    description='Pan-STARRS and ATLAS name server.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    version=__version__,
    author='genghisken',
    author_email='ken.w.smith@gmail.com',
    license='MIT',
    url='https://github.com/genghisken/gknames',
    packages=find_packages(),
    classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities',
    ],
    install_requires=[
          'mysqlclient',
          'django<4.2',
          'django-filter',
          'django_tables2',
          'markdown',
          'djangorestframework',
          'pyyaml',
          'docopt',
          'python-dotenv',
          'gkhtm',
          'gkutils>=0.2.22',
          'mod_wsgi',
      ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)
