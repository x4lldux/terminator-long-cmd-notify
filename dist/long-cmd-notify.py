"""
This plugin will launch a notification when a long running command finishes
and terminal is not active.

It uses VTE's special sequence which is sent when shell prints the prompt. It
depends on https://github.com/GNOME/vte/blob/vte-0-58/src/vte.sh (which has to
be added to /etc/profile.d) and you need to ensure `__vte_prompt_command` is
executed on `PROMPT_COMMAND` in Bash or in `precmd_functions` in Zsh.

Code is written in Hy and generated to Python3.
"""
import terminatorlib.plugin as plugin
from terminatorlib.terminator import Terminator
import gi
gi.require_version('Notify', '0.7')
from gi.repository import GObject, GLib, Notify
VERSION = '0.1.0'
AVAILABLE = ['LongCommandNotify']


class LongCommandNotify(plugin.Plugin):
    capabilities = ['command_watch']
    watched = {1}.__class__()

    def __init__(self):
        self.update_watched()
        Notify.init('Terminator')
        return None

    def update_watched(self, *_):
        """Updates the list of watched terminals"""
        _hyx_letXUffffX1 = {}
        _hyx_letXUffffX1['new-watched'] = {1}.__class__()
        for term in Terminator().terminals:
            _hyx_letXUffffX1['new-watched'].add(term)
            if not term in self.watched:
                _hyx_letXUffffX2 = {}
                _hyx_letXUffffX2['vte'] = term.get_vte()
                term.connect('focus-out', self.update_watched_delayed, None)
                _hyx_letXUffffX2['vte'].connect('focus-out-event', self.
                    update_watched_delayed, None)
                _hy_anon_var_2 = _hyx_letXUffffX2['vte'].connect(
                    'notification-received', self.notification_received, term)
            else:
                _hy_anon_var_2 = None
        self.watched = _hyx_letXUffffX1['new-watched']

    def update_watched_delayed(self, *_):

        def _hy_anon_var_4(self):
            self.update_watched()
            return False
        GObject.idle_add(_hy_anon_var_4, self)
        return True

    def notification_received(self, vte, summary, body, terminator_term):
        Notify.Notification.new(summary, body, 'terminator').show(
            ) if not vte.has_focus() else None
        return None

