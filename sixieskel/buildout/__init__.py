import os
from paste.script import copydir


def should_skip_file(name):
    """Overriding this just so we can include hidden files
    """
    if name.endswith('~') or name.endswith('.bak'):
        return 'Skipping backup file %(filename)s'
    if name.endswith('.pyc') or name.endswith('.pyo'):
        return 'Skipping %s file %%(filename)s' % os.path.splitext(name)[1]
    if name.endswith('$py.class'):
        return 'Skipping $py.class file %(filename)s'
    if name in ('CVS', '_darcs', '.svn', '.git', '.hg'):
        return 'Skipping version control directory %(filename)s'
    return None


copydir.should_skip_file = should_skip_file
