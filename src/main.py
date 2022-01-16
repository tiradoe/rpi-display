#!/usr/env/python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from views.default import DefaultView
from views.snapcontrol import SnapControlView

class AppWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="RPi Display")
        self.set_size_request(800,480)

        main_box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                )

        default_view = DefaultView()
        snapcontrol_view = SnapControlView()

        content_window = self.content_window()
        content_window.add_titled(default_view.generate_view(), "default_view", "Home")
        content_window.add_titled(snapcontrol_view.generate_view(), "snapcontrol_view", "Snapcast")

        switcher = Gtk.StackSwitcher(can_focus=False)
        switcher.set_name("menu")
        switcher.set_stack(content_window)

        main_box.pack_start(content_window, True, True, 0)
        main_box.pack_end(switcher, False, True, 0)

        self.load_css()
        self.add(main_box)

    def content_window(self):
        content_box = Gtk.Stack()

        content_box.set_transition_type(Gtk.StackTransitionType.OVER_UP)
        content_box.set_transition_duration(500)

        return content_box

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


window = AppWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
