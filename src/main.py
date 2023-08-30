# main.py
#
# Copyright 2023 Nokse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, Gdk
from .window import TacticsWindow

import threading

class TacticsApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.nokse22.tactics',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

        self.multiplayer_action = Gio.SimpleAction.new('multiplayer', None)
        self.multiplayer_action.connect("activate", self.on_multiplayer_action)
        self.add_action(self.multiplayer_action)

        self.singleplayer_action = Gio.SimpleAction.new('singleplayer', None)
        self.singleplayer_action.connect("activate", self.on_singleplayer_action)
        self.add_action(self.singleplayer_action)

        self.singleplayer_action.set_enabled(False)

        css = '''
        .small-grid {
            border: 5px solid @window_bg_color;
            background-color: @window_bg_color;
            padding: 10px;

        }
        .button {
            transition: background-color 0.5s ease-in, color 0.5s ease-in;
            padding: 5px;
            font-size: 140%;
        }
        .big-grid {
            background-color: @window_fg_color;
        }
        .won-1{
            border: 5px solid @destructive_color;
            transition: border 1s ease-in;
        }
        .won-2{
            border: 5px solid @accent_bg_color;
            transition: border 1s ease-in;
        }
        '''

        # box-shadow: 0px 0px 0px 2px #f66151;
        # border-radius: 10px;

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css, -1)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_singleplayer_action(self, widget, _):
        self.win.multyplayer = False
        self.singleplayer_action.set_enabled(False)
        self.multiplayer_action.set_enabled(True)

    def on_multiplayer_action(self, widget, _):
        self.win.multyplayer = True
        self.singleplayer_action.set_enabled(True)
        self.multiplayer_action.set_enabled(False)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = TacticsWindow(application=self)
        self.win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Tactics',
                                application_icon='io.github.nokse22.tactics',
                                developer_name='Nokse',
                                version='0.1.0',
                                developers=['Nokse'],
                                copyright='© 2023 Nokse')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = TacticsApplication()
    return app.run(sys.argv)
