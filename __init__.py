
import os, subprocess, pickle
from collections import namedtuple

plugin = namedtuple('plugin', 'name doc classpath sysproperty')

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

    def install(self, name, doc, plugin_, classpath, sysproperty = None):
        if sysproperty is None:
            sysproperty = []
        print 'installing %s plugin' % name
        print [os.path.abspath(path) for path in classpath]
        self._cfg[name] = \
            plugin(plugin_, doc,
                   [os.path.abspath(path)
                    for path in classpath],
                   [(n, os.path.abspath(v))
                     for n, v in sysproperty])

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
        plugin, doc, classpath, sysproperty = self._cfg[name]

        # Launch java with the appropriate classpath and main function
        cmd = ['java']
        cmd.extend(['-D%s=%s' % (name, value) for name, value in sysproperty])
        cmd.extend(['-cp', ':'.join(classpath), main, plugin])
        cmd.extend(args)
        try:
            ret = subprocess.call(cmd)
        except KeyboardInterrupt:
            print 'caught interrupt signal'
            ret = 1
        return ret

    @property
    def plugins(self):
        return [(name, plugin) for name, plugin in self._cfg.iteritems()]
