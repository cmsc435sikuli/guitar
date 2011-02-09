
import os, subprocess, pickle
from collections import namedtuple

plugin = namedtuple('plugin', 'name doc classpath')

class ui(object):
    def __init__(self, configPath = None):
        # Load configuration from file
        self._pathname = configPath
        self._cfg = {}
        if self._pathname is not None:
            try:
                with open(self._pathname, 'r') as f:
                    self._cfg = pickle.load(f)
            except:
                # Something went wrong reading the file, use defaults
                pass

    def __del__(self):
        if self._pathname is not None:
            with open(self._pathname, 'w') as f:
                pickle.dump(self._cfg, f)

    def install(self, name, doc, plugin_, classpath):
        print 'installing %s plugin' % name
        self._cfg[name] = plugin(plugin_, doc, [os.path.abspath(path)
                                                for path in classpath])

    def uninstall(self, name):
        if self._cfg.has_key(name):
            print 'uninstalling %s plugin' % name
            del self._cfg[name]
        else:
            print '%s plugin not installed (skipping)' % name

    def launch(self, main, name, *args):
        # Find java classpath and plugin from config
        if not self._cfg.has_key(name):
            print 'plugin %s not available' % name
            return 1
        plugin, doc, classpath = self._cfg[name]

        # Launch java with the appropriate classpath and main function
        cmd = ['java', '-cp', ':'.join(classpath), main, plugin]
        cmd.extend(args)
        return subprocess.call(cmd)

    @property
    def plugins(self):
        return [(name, plugin) for name, plugin in self._cfg.iteritems()]
