import os, re
from ConfigParser import SafeConfigParser

class TestFind():
    """
    This class is used to find any variant config files and list the
    tests that they contain.
    It walks the directory tree starting at ./ looking for any file
    with the extension .cfg.
    """
    def __init__(self):
        self.cfg_files = []
        self.variants_and_tests = []

    def getCfgs(self, path=None):
        cfg = re.compile(".*\.cfg$")
        if(path is None):
            path = '.'
            self.cfg_files = []
        else:
            path = os.path.normpath(path) # Removes extra /
        for directory, subdirs, files in os.walk(path):
            for f in files:
                found = cfg.search(f.strip())
                if(found is not None):
                    if(path is '.'):
                        self.cfg_files.append("%s%s%s" % (directory, os.sep, f))
                    else:
                        cfg_file = "%s%s%s" % (directory, os.sep, f)
                        self.cfg_files.append(cfg_file)
#                        self.read(self.cfg_file)
        print "Found the following config files"
        print "--------------------------------"
        for file in self.cfg_files:
            print "%s" % file
        print ""

    def buildTestStruct(self, path=None):
        """
        A list of dictionaries is used so that order is preserved.
        [
            {'variant0': {'path': ['test0', 'test1', 'test2',...]}},
            {'variant1': {'path': ['test0', 'test1', 'test2',...]}},
            {'variant2': {'path': ['test0', 'test1', 'test2',...]}},
        ]
        """
        self.getCfgs(path=path)
        if(len(self.cfg_files) > 0):
            for config in self.cfg_files:
                variant_name = None
                cfg = SafeConfigParser()
                cfg.read(config)
                if(cfg.has_option('DEFAULT', 'PROJ_ROOT')):
                    proj_root = cfg.get('DEFAULT', 'PROJ_ROOT')
                else:
                    proj_root = ''
                path = os.path.normpath(os.path.split(config)[0])

                    # Check the config file for a user supplied variant name
                if(cfg.has_option('DEFAULT', 'VARIANT_NAME')):
                    variant_name = cfg.get('DEFAULT', 'VARIANT_NAME')

                    # If the user supplied a variant name then use it
                    # or use the directory name instead
                if(variant_name is None):
                    if(path == '.'):    # Use the directory name as the variant_name
                        variant_name = os.path.normpath(os.path.split(os.getcwd())[1])
                    else:
                        variant_name = path
#                print "Path: %s/" % (path)
#                print "Config: %s" % (config)
#                print "Variant: %s" % (variant_name)
#                print ""
                a = cfg.sections()
                a.sort()
                self.variants_and_tests.append({variant_name: {path: a}})
        for i in self.variants_and_tests:
            for v in i:                     # Variant
#                print "Variant: %s" % v
                for p in i[v]:              # Path
                    print "%s/" % p
                    for t in i[v][p]:       # Tests
                        print "    %s" % t
            print ""

    def listTests(self):
        """
        List all available tests from the current working directory down.
        """
        self.getCfgs()
        if(len(self.cfg_files) > 0):
            for config in self.cfg_files:
                cfg = SafeConfigParser()
                cfg.read(config)
                if(cfg.has_option('DEFAULT', 'PROJ_ROOT')):
                    proj_root = cfg.get('DEFAULT', 'PROJ_ROOT')
                else:
                    proj_root = ''
                path = os.path.normpath(os.path.split(config)[0])
                print "%s/" % (path) #, cfg.cp.get('DEFAULT', 'VARIANT_NAME'))
                a = cfg.sections()
                a.sort()
                for section in a:
                    print "    %s" % section
        print ""
        print "To run a simulation:"
        print "simulate <path_to/variant>/<test>"
        print ""
        print "Example:"
        if(path == "."):
            print "    sim %s" % (a[0])
        else:
            print "    sim %s/%s" % (path, a[0])
        print ""


