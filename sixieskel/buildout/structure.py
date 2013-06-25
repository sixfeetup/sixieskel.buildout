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
