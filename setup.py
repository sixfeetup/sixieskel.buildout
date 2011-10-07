from setuptools import setup, find_packages

version = '1.0.2'

setup(
    name='sixieskel.buildout',
    version=version,
    description="",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='web zope command-line skeleton project',
    author='Six Feet Up, Inc.',
    author_email='info@sixfeetup.com',
    url='http://www.sixfeetup.com',
    namespace_packages=['sixieskel'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "templer.buildout",
    ],
    entry_points="""
    [paste.paster_create_template]
    sfu_buildout = sixieskel.buildout.template:SixieBuildout
    """,
    )
