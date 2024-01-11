from kabaret.app import plugin
from kabaret.app.actors.flow.actor import ProjectRoot
from kabaret.app.ui.gui.widgets.flow.flow_view import QtWidgets, FlowView, FlowPage, CustomPageHost
from kabaret.app.ui.gui.widgets.flow.script_line import ScriptLine
from kabaret.app.ui.gui.widgets.flow.flow_form import FlowForm
from kabaret.app.ui.gui.widgets.flow.navigator import Navigator
from kabaret.app.ui.gui.widgets.flow.navigation_control import (
    NavigationOIDControls
)
from kabaret.app.ui.view import ViewMixin
from kabaret.app import resources

from ...search.view import SearchSettingsDialog
from ...search.data import icons as _

from ....resources.icons import gui as _

from .navigation_control import NavigationBar


class DefaultFlowPage(FlowPage):

    def __init__(self, parent, view, start_oid, root_oid):
        super(FlowPage, self).__init__(parent)

        self.view = view
        self.session = view.session

        self._navigator = Navigator(
            self.session, root_oid, start_oid
        )
        self._navigator.set_create_view_function(view.create_view)

        self.nav_bar = NavigationBar(self, self._navigator)
        self.nav_ctrl = self.nav_bar.nav_ctrl
        self.nav_oid = self.nav_bar.nav_oid_bar.nav_oid
        self.nav_oid_field = self.nav_bar.nav_oid_bar.nav_oid_field

        self.custom_page_host = CustomPageHost(self)
        self.custom_page_host.hide()
        self.form = FlowForm(self, self)

        lo = QtWidgets.QVBoxLayout()
        lo.addWidget(self.nav_bar)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)
        lo.addWidget(self.form, 100)
        lo.addWidget(self.custom_page_host, 100)

        self._navigator.add_on_current_changed(self.refresh)

        self._source_view_id = None
    
    def refresh(self):
        oid = self.current_oid()
        view_title = self.session.cmds.Flow.get_source_display(oid)
        self.view.set_view_title(view_title)

        self.clear()

        self.nav_oid.update_controls()
        self.nav_ctrl.update_controls()

        ui = self.session.cmds.Flow.get_object_ui(oid)
        self.view.set_show_navigation_bar(ui.get('navigation_bar', True))
        
        custom_page = ui.get('custom_page')
        if self.view.login_check:
            if self.show_login_page(oid):
                custom_page = 'libreflow.baseflow.LoginPageWidget'

        if custom_page:
            self.custom_page_host.host(oid, custom_page)
            self.form.hide()
        else:
            self.custom_page_host.unhost()
            self.form.show()
            self.form.build_roots(oid)

    def show_login_page(self, oid):
        # Check if root is a Project
        o = self.session.get_actor('Flow').get_object(oid)
        root = o.root()
        if type(root) is ProjectRoot:
            if root.project().show_login_page():
                return True
        
        return False


class DefaultFlowView(FlowView):

    def __init__(self, session, view_id=None, hidden=False, area=None, oid=None, root_oid=None):
        self._start_oid = oid
        self._root_oid = root_oid
        self.options_menu = None
        self.dev_menu = None
        self.script_line = None
        self.flow_page = None
        self.login_check = True

        try:
            parent = session.main_window_manager.main_window
        except AttributeError:
            raise TypeError(
                'The "%s" view cannont be used in a session without a main_window'%(
                    self.__class__.__name__
                )
            )
        ViewMixin.__init__(self, session, view_id)
        QtWidgets.QWidget.__init__(self, None)

        self._main_window_manager = session.main_window_manager

        # Menu
        self.view_menu = QtWidgets.QMenu(self.view_title())

        # Tools
        self._header_tools = {}
        self._header_tools_layout = QtWidgets.QHBoxLayout()

        content_widget = QtWidgets.QWidget(self)

        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)

        hlo = QtWidgets.QHBoxLayout()
        hlo.setContentsMargins(0, 0, 0, 0)
        header_widgets_layout = QtWidgets.QHBoxLayout()
        hlo.addStretch()
        hlo.addLayout(header_widgets_layout, 100)
        hlo.addLayout(self._header_tools_layout)
        lo.addLayout(hlo)
        top_layout = QtWidgets.QHBoxLayout()
        lo.addLayout(top_layout)
        lo.addWidget(content_widget, 100)
        self._build(
            self, top_layout, content_widget,
            self, header_widgets_layout
        )

        self._update_menus()

        dock = self._main_window_manager.create_docked_view_dock(self, hidden=hidden, area=area)

        # This is needed for layout state
        # Multi instance view types must use another policy
        dock.setObjectName(self.view_id())
    
    def build_top(self, top_parent, top_layout, header_parent, header_layout):
        self.options_menu = self.view_menu.addMenu('Options')

        a = self.options_menu.addAction('Show Navigation Bar')
        a.setCheckable(True)
        a.setChecked(True)
        a.toggled.connect(self.set_show_navigation_bar)
        self._show_nav_bar_action = a

        a = self.options_menu.addAction('Show Hidden Relations')
        a.setCheckable(True)
        a.setChecked(False)
        a.toggled.connect(self.set_show_hidden_relations)

        a = self.options_menu.addAction('Show References')
        a.setCheckable(True)
        a.setChecked(False)
        a.toggled.connect(self.set_show_references_relations)

        self.options_menu.addAction('Create New View')
        self.options_menu.addSeparator()
        self.options_menu.addAction(
            'Activate DEV Tools',
            self._activate_dev_tools
        )

        self.script_line = ScriptLine(top_parent, self)
        self.script_line.hide()
        top_layout.addWidget(self.script_line, 100)

        # Search bar
        if self.session._search_index_uri is not None:
            self.search_dialog = SearchSettingsDialog(top_parent, self.session)
            self.options_menu.addSeparator()
            self.options_menu.addAction(
                resources.get_icon(('icons.search', 'magn-glass')),
                'Search settings',
                self._show_search_options
            )

    def build_page(self, main_parent):
        self.flow_page = DefaultFlowPage(
            main_parent, self, self._start_oid, self._root_oid
        )

        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.addWidget(self.flow_page)
        self.flow_page.show()

        main_parent.setLayout(lo)
        self.flow_page.refresh()

    def toggle_login_check(self):
        self.login_check = False if self.login_check else True
        self.flow_page.refresh()
    
    def _activate_dev_tools(self):
        if self.dev_menu is not None:
            return
        self.dev_menu = self.view_menu.addMenu('[DEV]')

        self.dev_menu.addAction('Toggle Script Line', self.toggle_script_line)

        a = self.view_menu.addAction('Group Relations')
        a.setCheckable(True)
        a.setChecked(True)
        a.toggled.connect(self.set_group_relations)

        a = self.dev_menu.addAction('Show Protected Relations')
        a.setCheckable(True)
        a.setChecked(False)
        a.toggled.connect(self.set_show_protected_relations)

        a = self.dev_menu.addAction('Toggle Kitsu Login')
        a.setCheckable(True)
        a.setChecked(self.login_check)
        a.toggled.connect(self.toggle_login_check)

        self.dev_menu.addSeparator()

        self.dev_menu.addAction('Reload Projects Definition', self.reload_projects)

        self.toggle_script_line()

    def _show_search_options(self):
        self.search_dialog.show()


class DefaultFlowViewPlugin:
    """
    Default Flow view.

    Will only be installed if no other view
    is registered under the "Flow" view type name.
    """

    @plugin(trylast=True)
    def install_views(session):
        if not session.is_gui():
            return

        type_name = DefaultFlowView.view_type_name()
        if not session.has_view_type(type_name):
            session.register_view_type(DefaultFlowView)
            session.add_view(type_name)
