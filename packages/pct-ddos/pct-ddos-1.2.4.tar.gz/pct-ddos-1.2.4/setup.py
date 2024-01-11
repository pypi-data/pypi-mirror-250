from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pct-ddos',
    version='1.2.4',
    description='PCT DDOS is a tool for carrying out DDOS attacks which cause the target website to go down. This tool was developed or created by the Palembang Cyber Team.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Palembang Cyber Team',
    author_email='',
    url='https://whatsapp.com/channel/0029VaFBBJBBfxo0tIHYMi3r',
    packages=['pctddos'],
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
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6',
    install_requires=[
      'requests-futures',
      'requests',
      'pychalk',
      'asyncio',
      'pymongo',
      'dnspython',
      'pytz',
      'pycryptodome'
    ],
)
