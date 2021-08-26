from setuptools import setup, find_packages

setup(
    name='django-admin-kit',
    version='0.0.17',
    description='Django Admin Kit provides additional features to Django Admin',
    author='Rohan Poojary',
    author_email='rohanrp23@gmail.com',
    url='https://github.com/RohanPoojary/django-admin-kit',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
    license='MIT',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.11',
    ],
)
