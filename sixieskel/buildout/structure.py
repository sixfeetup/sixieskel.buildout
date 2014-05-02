from templer.core.structures import Structure


class FabFileStructure(Structure):
    """Simple structure to add a sixfeetup.deployment fab file
    """
    _structure_dir = 'structures/fabfile'


class Bootstrap2(Structure):
    """Simple structure to add a bootstrap.py file for buildout v2
    """
    _structure_dir = 'structures/bootstrap2'


class BuildoutHttp(Structure):
    """Simple structure to add a .httpauth file
    """
    _structure_dir = 'structures/buildouthttp'


class UnifiedBuildout(Structure):
    """If we are creating a unified buildout, include a setup.py
    """
    _structure_dir = 'structures/unified'


class ContentPackage(Structure):
    """Structure to set up a unified buildout, so custom packages
       are in the same repo as the buildout
    """
    _structure_dir = 'structures/content'


class PolicyPackage(Structure):
    """Structure to set up a unified buildout, so custom packages
       are in the same repo as the buildout
    """
    _structure_dir = 'structures/policy'


class ThemePackage(Structure):
    """Structure to set up a unified buildout, so custom packages
       are in the same repo as the buildout
    """
    _structure_dir = 'structures/theme'