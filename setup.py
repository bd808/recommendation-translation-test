from setuptools import setup, find_packages

setup(
    name='recommendation_translation_test',
    version='0.0.2',
    url='https://github.com/schana/recommendation-translation-test',
    license='Apache Software License',
    maintainer='Wikimedia Research',
    maintainer_email='nschaaf@wikimedia.org',
    description='Provide translation recommendations',
    long_description='',
    packages=find_packages(exclude=['test', 'test.*', '*.test']),
    install_requires=['recommendation',
                      'flask',
                      'flask-restplus',
                      'psycopg2'],
    package_data={'recommendation_translation_test': ['data/*']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest',
                   'responses'])
