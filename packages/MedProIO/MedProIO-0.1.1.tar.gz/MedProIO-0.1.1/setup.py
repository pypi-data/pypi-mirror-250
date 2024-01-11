from setuptools import setup

setup(
    name='MedProIO',
    version='0.1.1',    
    description='A package to perform specific Medical Image processing operations based on SimpleITK',
    url='',
    author='Dimitris Zaridis',
    author_email='dimzaridis@gmail.com',
    license='MIT',
    packages=['MedProIO'],
    install_requires=["SimpleITK==2.3.1",
                    "numpy==1.26.2"                    
                    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',       
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)