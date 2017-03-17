from setuptools import setup, find_packages

setup(
    name='recommendation_missing_sections',
    version='0.0.4',
    url='https://github.com/schana/recommendation-missing-sections',
    license='Apache Software License',
    maintainer='Wikimedia Research',
    maintainer_email='nschaaf@wikimedia.org',
    description='Provide missing section recommendations',
    long_description='',
    packages=find_packages(exclude=['test', 'test.*', '*.test']),
    install_requires=['recommendation',
                      'flask',
                      'flask-restplus',
                      'pymongo'],
    package_data={'recommendation_missing_sections': ['data/*']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest',
                   'responses'])

