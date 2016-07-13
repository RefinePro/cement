"""Tests for cement.ext.ext_watchdog."""

import os
from cement.utils import test
from cement.core.exc import FrameworkError
from cement.ext.ext_watchdog import WatchdogEventHandler


class MyEventHandler(WatchdogEventHandler):
    pass

class WatchdogExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(WatchdogExtTestCase, self).setUp()
        self.app = self.make_app('tests',
                                 extensions=['watchdog'],
                                 argv=[]
                                 )

    def test_watchdog(self):
        self.app.setup()
        self.app.watchdog.add(self.tmp_dir, event_handler=MyEventHandler)
        self.app.run()

        # trigger an event
        f = open(os.path.join(self.tmp_dir, 'test.file'), 'w')
        f.write('test data')
        f.close()

        self.app.close()

    def test_watchdog_app_paths(self):
        self.reset_backend()
        self.app = self.make_app('tests',
                                 extensions=['watchdog'],
                                 argv=[]
                                 )
        self.app._meta.watchdog_paths = [
            (self.tmp_dir),
            (self.tmp_dir, WatchdogEventHandler)
        ]
        self.app.setup()
        self.app.run()

        # trigger an event
        f = open(os.path.join(self.tmp_dir, 'test.file'), 'w')
        f.write('test data')
        f.close()
        
        self.app.close()

    @test.raises(FrameworkError)
    def test_watchdog_app_paths_bad_spec(self):
        self.reset_backend()
        self.app = self.make_app('tests',
                                 extensions=['watchdog'],
                                 argv=[]
                                 )
        self.app._meta.watchdog_paths = [
            [self.tmp_dir, WatchdogEventHandler]
        ]
        self.app.setup()

    def test_watchdog_default_event_handler(self):
        self.app.setup()
        self.app.watchdog.add(self.tmp_dir)
        self.app.run()
        self.app.close()

    def test_watchdog_bad_path(self):
        self.app.setup()
        self.app.watchdog.add(os.path.join(self.tmp_dir, 'bogus_sub_dir'))
        self.app.run()
        self.app.close()
