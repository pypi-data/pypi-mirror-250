import sys
import os
import argparse

os.environ['QT_MAC_WANTS_LAYER'] = '1'

from qtpy import QtCore
from kabaret.app.ui import gui
from kabaret.app.actors.flow import Flow
from kabaret.subprocess_manager import SubprocessManager

from libreflow.resources.icons import libreflow, status
from libreflow.resources import file_templates
from libreflow.utils.kabaret.ui.flow_view import DefaultFlowViewPlugin
from libreflow.utils.kabaret.ui.main_window import DefaultMainWindowManager
from libreflow.utils.search.actor import Search
import libreflow.utils.kabaret as kutils


CUSTOM_HOME = True
DEBUG = False
SCRIPT_VIEW = True
JOBS_VIEW = True
SEARCH_ENABLED = True

try:
    from kabaret.script_view import script_view
except ImportError:
    SCRIPT_VIEW = False

try:
    from libreflow.utils.kabaret.jobs.jobs_view import JobsView
    from libreflow.utils.kabaret.jobs.jobs_actor import Jobs
except ImportError:
    print('ERROR: kabaret.jobs not found')
    JOBS_VIEW = False

if CUSTOM_HOME:
    from .custom_home import MyHomeRoot

from .resources import file_templates, gifs


try:
    from libreflow.resources.styles.lfs_tech import LfsTechStyle  
except ImportError:
    from .resources.gui.styles.default_style import DefaultStyle
    DefaultStyle()
else:
    LfsTechStyle()



class SessionGUI(gui.KabaretStandaloneGUISession):

    def __init__(self, session_name='Standalone', tick_every_ms=10, debug=False, search_index_uri=None, search_auto_indexing=False):
        self._search_index_uri = search_index_uri
        self._search_auto_indexing = search_auto_indexing
        super(SessionGUI, self).__init__(session_name, tick_every_ms, debug)
    
    def register_plugins(self, plugin_manager):
        super(gui.KabaretStandaloneGUISession, self).register_plugins(plugin_manager)
        
        # Register libreflow default view plugin
        plugin_manager.register(DefaultFlowViewPlugin, 'kabaret.flow_view')
    
    def create_window_manager(self):
        return DefaultMainWindowManager.create_window(self)

    def register_view_types(self):
        super(SessionGUI, self).register_view_types()

        if SCRIPT_VIEW:
            type_name = self.register_view_type(script_view.ScriptView)
            self.add_view(
                type_name, hidden=not DEBUG, area=QtCore.Qt.RightDockWidgetArea
            )
            type_name = self.register_view_type(kutils.subprocess_manager.SubprocessView)
            self.add_view(
                type_name,
                view_id='Processes',
                hidden=not DEBUG,
                area=QtCore.Qt.RightDockWidgetArea,
            )

        if JOBS_VIEW:
            type_name = self.register_view_type(JobsView)
            self.add_view(
                type_name,
                hidden=not DEBUG,
                area=QtCore.Qt.RightDockWidgetArea,
            )

    def _create_actors(self):
        '''
        Instanciate the session actors.
        Subclasses can override this to install customs actors or
        replace default ones.
        '''
        if CUSTOM_HOME:
            Flow(self, CustomHomeRootType=MyHomeRoot)
        else:
            return super(SessionGUI, self)._create_actors()
        subprocess_manager = kutils.subprocess_manager.SubprocessManager(self)

        jobs = Jobs(self)

        if SEARCH_ENABLED and self._search_index_uri is not None:
            Search(self, self._search_index_uri, self._search_auto_indexing)


def process_remaining_args(args):
    parser = argparse.ArgumentParser(
        description='Libreflow Session Arguments'
    )
    parser.add_argument(
        '-u', '--user', dest='user'
    )
    parser.add_argument(
        '-s', '--site', default='LFS', dest='site'
    )
    parser.add_argument(
        '-j', '--jobs_default_filter', dest='jobs_default_filter'
    )
    parser.add_argument(
        '--search-index-uri', dest='search_index_uri'
    )
    parser.add_argument(
        '--search-auto-indexing', dest='search_auto_indexing', nargs='?', const=True, type=bool
    )
    values, _ = parser.parse_known_args(args)

    if values.site:
        os.environ['KABARET_SITE_NAME'] = values.site
    if values.user:
        os.environ['USER_NAME'] = values.user
    if values.jobs_default_filter:
        os.environ['JOBS_DEFAULT_FILTER'] = values.jobs_default_filter
    else:
        os.environ['JOBS_DEFAULT_FILTER'] = values.site
    
    if values.search_auto_indexing is None:
        values.search_auto_indexing = 'SEARCH_AUTO_INDEXING' in os.environ
    
    return values.search_index_uri, values.search_auto_indexing


def main(argv):
    (
        session_name,
        host,
        port,
        cluster_name,
        db,
        password,
        debug,
        remaining_args,
    ) = SessionGUI.parse_command_line_args(argv)

    uri, auto_indexing = process_remaining_args(remaining_args)

    session = SessionGUI(session_name=session_name, debug=debug, search_index_uri=uri, search_auto_indexing=auto_indexing)
    session.cmds.Cluster.connect(host, port, cluster_name, db, password)

    session.start()
    session.close()


if __name__ == '__main__':
    main(sys.argv[1:])