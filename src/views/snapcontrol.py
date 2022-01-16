import gi
import asyncio
import snapcast.control

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from dotenv import dotenv_values

class SnapControlView(Gtk.FlowBox):
    def __init__(self):
        self.row_name = "Snapcontrol"
        self.loop = asyncio.get_event_loop()
        self.config = dotenv_values(".env")
        self.server = self.loop.run_until_complete(
                snapcast.control.create_server(
                    self.loop,
                    self.config["SNAPCAST_IP"],
                    self.config["SNAPCAST_CONTROL_PORT"])
                )

    def generate_view(self):
        display = Gtk.FlowBox(  )

        display.set_valign(Gtk.Align.START)
        display.set_max_children_per_line(3)
        display.set_selection_mode(Gtk.SelectionMode.NONE)
        display.set_name("snapcontrol-grid")

        display.set_valign(True)
        display.set_vexpand(True)
        display.set_hexpand(True)

        self.get_group_list(display)

        return display


    def get_group_list(self, flowbox):

        for group in self.server.groups:
            group_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            group_box.set_name("group-box")

            group_header_box = Gtk.Box()
            group_header_box.set_name("group-header")

            group_switch = Gtk.Switch()
            group_switch.set_name("switch")
            group_switch.connect("notify::active", self.on_mute_toggle, {"type": "group", "group": group})
            group_switch.set_state(not group.muted)

            group_name = Gtk.Label(group.friendly_name)

            group_header_box.pack_start(group_name, False, False, 20)
            group_header_box.pack_end(group_switch, False, False, 1)


            group_box.pack_start(group_header_box, False, False, 1)

            for client_name in group.clients:
                client_box = Gtk.Box()
                client_box.set_name("client-box")

                client_switch = Gtk.Switch()
                client_switch.connect("notify::active", self.on_mute_toggle,  {"type": "client", "client": client_name})
                client_switch.set_state(not self.server.client(client_name).muted)

                name = Gtk.Label(self.server.client(client_name).friendly_name)

                client_box.pack_start(name, False, False, 20)
                client_box.pack_end(client_switch, False, False, 1)

                group_box.pack_start(client_box, False, False, 1)

            flowbox.add(group_box)

    def set_volume(self, volume):
        # set volume for client #0 to 50%
        client = self.server.clients[1]
        self.loop.run_until_complete(self.server.client_volume(
            client.identifier, {
                'percent': volume,
                'muted': False
                })
            )

    def on_mute_toggle(self, switch, gparam, player):
        if(player["type"] == 'group'):
            self.loop.run_until_complete(
                self.server.group_mute( player["group"].identifier,
                not switch.get_state()
            ))
        else:
            self.loop.run_until_complete(self.server.client_volume(
                player["client"], {
                    'muted': not switch.get_state()
                    }
                ))


