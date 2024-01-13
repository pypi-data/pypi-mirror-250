from setuptools import setup, find_packages

setup(
    name='crossmdf',
    version='0.1.0',
    packages=find_packages(),  # 'where' parameter is not needed if the code is in the root of the package
    license='MIT',
    description='An utility for fusing data across different modalities like text and image',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important for README.md to be displayed correctly on PyPI
    author='Hiromu Abe',
    author_email='s2122072@stu.musashino-u.ac.jp',
    url='https://github.com/Hiromuabe/cromdf',  # Replace with the actual URL
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'torch',
        'torchvision'
    ],
    python_requires='>=3.6',  # Specify the minimum required Python version
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='data fusion, multimodal, text features, image features',  # Keywords for your package
    project_urls={  # Optional
        'Source': 'https://github.com/Hiromuabe/cromdf/',
    },
)
