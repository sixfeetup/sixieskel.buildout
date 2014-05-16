from setuptools import setup, find_packages

version = '1.5.3'

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
    sfu_pyramid_buildout = sixieskel.buildout.template:SixiePyramidBuildout
    sfu_pyramid_zodb_buildout = sixieskel.buildout.template:SixiePyramidZodbBuildout

    [templer.templer_structure]
    sixie_fabfile = sixieskel.buildout.structure:FabFileStructure
    buildouthttp = sixieskel.buildout.structure:BuildoutHttp
    bootstrap2 = sixieskel.buildout.structure:Bootstrap2
    unified = sixieskel.buildout.structure:UnifiedBuildout
    content_pkg = sixieskel.buildout.structure:ContentPackage
    policy_pkg = sixieskel.buildout.structure:PolicyPackage
    theme_pkg = sixieskel.buildout.structure:ThemePackage
    """,
    )
