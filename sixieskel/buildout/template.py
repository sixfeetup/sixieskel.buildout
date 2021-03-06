import copy
import os
import subprocess
from templer.core.base import BaseTemplate
from templer.core.vars import EXPERT
from templer.core.vars import BooleanVar
from templer.core.vars import IntVar
from templer.core.vars import StringVar

# list of files to ignore in git or svn
IGNORE_FILES = [
    '# ignoring these files/dirs in the buildout',
    'develop-eggs',
    'fake-eggs',
    'eggs',
    'bin',
    'var',
    'parts',
    'downloads',
    'products',
    'src',
    '.installed.cfg',
    'dumped-versions.cfg',
    'tags',
    '.mr.developer.cfg',
    'buildout.cfg',
]


def run_cmd(cmd):
    """Run a command and get back the output
    """
    ret = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE
        ).communicate()
    return ret[0][:-1]


class SixieBuildout(BaseTemplate):
    _template_dir = 'templates/buildout'
    summary = "A Plone 3.x+ buildout following the Six Feet Up standards"
    category = "Six Feet Up"
    default_required_structures = ['sixie_fabfile']
    required_templates = []
    use_cheetah = True
    vars = copy.deepcopy(BaseTemplate.vars)
    vars.extend([
        StringVar(
            'site_name',
            'Plone site name',
            default='Plone',
        ),
        StringVar(
            'project_name',
            'Project name (used for dist and fabric setup)',
        ),
        StringVar(
            'plone_version',
            'Plone version (enter 3.1 to get the old style install)',
            default='4.3.7',
            ),
        IntVar(
            'local_port_offset',
            'Local project port number (to be added to the base number)',
            default=0,
        ),
        StringVar(
            'zope_user',
            'Zope root admin user',
            default='admin',
        ),
        StringVar(
            'zope_password',
            'Zope root admin password '
            '(will be generated if left blank, requires pwgen)',
        ),
        IntVar(
            'http_port_base',
            'HTTP port (51000 range)',
            default=51000,
            modes=(EXPERT,),
        ),
        IntVar(
            'zeo_port_base',
            'ZEO port (53000 range)',
            default=53000,
            modes=(EXPERT,),
        ),
        IntVar(
            'ftp_port_base',
            'FTP port (52000 range)',
            default=52000,
            modes=(EXPERT,),
        ),
        StringVar(
            'effective_user',
            'Effective user (for dev/maint)',
            default='zope',
            modes=(EXPERT,),
        ),
        BooleanVar(
            'unified_buildout',
            'Is this a unified buildout?',
            default='yes',
        ),
        BooleanVar(
            'include_content',
            'Add a content package?',
            default='yes',
        ),
        BooleanVar(
            'include_policy',
            'Add a policy package?',
            default='yes',
        ),
        BooleanVar(
            'include_theme',
            'Add a theme package?',
            default='yes',
        ),
        StringVar(
            'staff_password',
            'Enter the Staff password (leave blank for auto generated)',
            modes=(EXPERT,),
        ),
    ])

    def check_vars(self, vars, cmd):
        result = BaseTemplate.check_vars(self, vars, cmd)
        if not vars['zope_password']:
            # for this to work you'll need pwgen installed
            passwd = run_cmd('pwgen -acn 9 1')
            if not passwd:
                passwd = 'admin'
            result['zope_password'] = passwd
        if not vars['staff_password']:
            # for this to work you'll need pwgen installed
            passwd = run_cmd('pwgen -acn 9 1')
            if not passwd:
                passwd = 'changeme'
            result['staff_password'] = passwd
        if int(result['plone_version'].split('.')[0]) < 4:
            self.required_structures.append('bootstrap')
        if vars['unified_buildout']:
            self.required_structures.append('unified')
        if vars['include_content']:
            self.required_structures.append('content_pkg')
        if vars['include_policy']:
            self.required_structures.append('policy_pkg')
        if vars['include_theme']:
            self.required_structures.append('theme_pkg')
        # XXX: var.structures can't handle this case yet
        if vars['project_name']:
            self.required_structures.append('buildouthttp')
        return result

    def _buildout(self, output_dir):
        os.chdir(output_dir)
        print "Bootstrapping the buildout"
        subprocess.call(["python", "bootstrap.py"])
        print "Configuring the buildout"
        subprocess.call(["bin/buildout", "-n"])

    def post(self, command, output_dir, vars):
        output_dir = os.path.abspath(output_dir)
        # make the control script executable
        os.chmod(os.path.join(output_dir, "scripts", "control"), 0755)
        os.chmod(os.path.join(output_dir, "scripts", "release.sh"), 0755)
        project_name = vars['project_name']
        # this is evil, I apologize. Paster can't handle .files in templates.
        ignore_fp = os.path.join(output_dir, "IGNORE.txt")
        ignore_file = open(ignore_fp, "w")
        gitignore_fp = os.path.join(output_dir, ".gitignore")
        gitignore_file = open(gitignore_fp, "w")
        ignore_file.write("""\
# Set with:
#   svn propset svn:ignore -F IGNORE.txt .
#
""")
        ignore_file.write("\n".join(IGNORE_FILES))
        # ignore the git ignore file
        ignore_file.write("\n.gitignore")
        gitignore_file.write("\n".join(IGNORE_FILES))
        # ignore the svn ignore file
        gitignore_file.write("\nIGNORE.txt")
        ignore_file.close()
        gitignore_file.close()
        if '.svn' in os.listdir(output_dir):
            subprocess.call('svn add %s' % ignore_fp, shell=True)
        # if we used the --svn-repo switch then check it in
        if '.svn' in os.listdir(output_dir):
            os.chdir(output_dir)

            subprocess.call(
                'svn ps svn:executable ON ./scripts/control',
                shell=True
                )

            subprocess.call(
                'svn ps svn:executable ON ./scripts/release.sh',
                shell=True
                )
            subprocess.call('svn ps svn:ignore -F IGNORE.txt .', shell=True)
            subprocess.call(
                'svn ps svn:ignore -F src/IGNORE.txt src', shell=True)

            msg = '"Checking in initial buildout for %s"' % vars['project']
            subprocess.call(
                'svn ci -m %s' % msg,
                shell=True
                )

            os.chdir('../')
        print "-----------------------------------------------------------"
        print
        print "Generation finished"
        print "You probably want to run python bootstrap.py and then"
        print "run bin/buildout -v"
        print
        print "See README.txt for details"
        print
        if project_name:
            print "NOTE: YOU NEED A PRIVATE DIST PASSWORD, ASK A PIRATE."
            print "      Then place the password in %s/.httpauth" % output_dir
            print
        print "Configuration summary:"
        print "  Zope admin user    : %s" % vars['zope_user']
        print "  Zope admin password: %s" % vars["zope_password"]
        print "  staff password: %s" % vars["staff_password"]
        print "  ^ change this in policy/setuphandlers.py if necessary "
        print "-----------------------------------------------------------"


class SixiePyramidBuildout(BaseTemplate):
    _template_dir = 'templates/pyramid_buildout'
    summary = "A Pyramid buildout following Six Feet Up Standards."
    category = "Six Feet Up"
    default_required_structures = ['sixie_fabfile']
    required_templates = []
    use_cheetah = True
    vars = copy.deepcopy(BaseTemplate.vars)
    vars.extend([
        StringVar(
            'project_name',
            'Project name (used for dist and fabric set up)',
        ),
        IntVar(
            'local_port_offset',
            'Local project port number (to be added to the base number)',
            default=0,
        ),
        IntVar(
            'http_port_base',
            'HTTP port (51000 range)',
            default=51000,
            modes=(EXPERT,),
        ),
        IntVar(
            'zeo_port_base',
            'Base zeoserver port.',
            default=53000,
            modes=(EXPERT,),
        ),
    ])

    def check_vars(self, vars, cmd):
        result = BaseTemplate.check_vars(self, vars, cmd)
        if vars['project_name']:
            self.required_structures.append('buildouthttp')
        return result

    def _buildout(self, output_dir):
        os.chdir(output_dir)
        print "Bootstrapping the buildout"
        subprocess.call(["python", "bootstrap.py"])
        print "Configuring the buildout"
        subprocess.call(["bin/buildout", "-n"])

    def post(self, command, output_dir, vars):
        output_dir = os.path.abspath(output_dir)
        os.chmod(os.path.join(output_dir, "scripts", "release.sh"), 0755)
        project_name = vars['project_name']
        # this is evil, I apologize. Paster can't handle .files in templates.
        gitignore_fp = os.path.join(output_dir, ".gitignore")
        gitignore_file = open(gitignore_fp, "w")
        gitignore_file.write("\n".join(IGNORE_FILES))
        gitignore_file.close()
        print "-----------------------------------------------------------"
        print
        print "Generation finished"
        print "You probably want to run python bootstrap.py and then"
        print "run bin/buildout -v"
        print
        print "See README.txt for details"
        print
        if project_name:
            print "NOTE: YOU NEED A PRIVATE DIST PASSWORD, ASK A PIRATE."
            print "      Then place the password in %s/.httpauth" % output_dir
            print


class SixiePyramidZodbBuildout(SixiePyramidBuildout):
    _template_dir = 'templates/pyramid_zodb_buildout'
    summary = "A Pyramid buildout following Six Feet Up Standards, \
               using ZODB for persistence."
