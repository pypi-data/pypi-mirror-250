from setuptools import setup, find_packages

setup(
    name='rams',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            # If your package includes any command-line scripts, list them here
        ],
    },
    author='kumar',
    author_email='your.email@example.com',
    description='A brief description of your package',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package_name',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
