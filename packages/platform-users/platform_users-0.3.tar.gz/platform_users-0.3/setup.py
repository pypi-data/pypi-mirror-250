from setuptools import setup, find_packages

setup(
    name='platform_users',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'Django>=3.1',
        'djangorestframework>=3.11.1'
        # Add other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
