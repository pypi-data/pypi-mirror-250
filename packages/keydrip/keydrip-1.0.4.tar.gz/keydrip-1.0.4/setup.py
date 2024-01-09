from setuptools import setup, find_packages

setup(
    name='keydrip',
    version='1.0.4',
    description='This is the first customizable Keydrop library bypassing its cloudflare, cybervio and steam. It\'s not revolutionary, but can be used to create a lot of tools!',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',  # Added to specify the content type of the README
    author='abdurryy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.4',
    install_requires=[
        'pyyaml',
        'cloudscraper',
        'beautifulsoup4'
    ],
    url='https://github.com/abdurryy/Keydrip',
    project_urls={
        'Homepage': 'https://github.com/abdurryy/Keydrip',
        'Issues': 'https://github.com/abdurryy/Keydrip/issues'
    }
)
