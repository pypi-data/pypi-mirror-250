from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='whoid_api',
    version='0.0.1',
    author='sl1pper',
    author_email='averin_sd@icloud.com',
    description='API to the unified authorization system WhoID (whoid.ru)',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/sl1pperq/whoid-api',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='id 1561 auth',
    project_urls={
        'GitHub': 'https://github.com/sl1pperq/whoid-api'
    },
    python_requires='>=3.6'
)
