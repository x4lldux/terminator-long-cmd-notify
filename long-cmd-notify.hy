"
This plugin will launch a notification when a long running command finishes
and terminal is not active.

It uses VTE's special sequence which is sent when shell prints the prompt. It
depends on https://github.com/GNOME/vte/blob/vte-0-58/src/vte.sh (which has to
be added to /etc/profile.d) and ensure `__vte_prompt_command` is executed on
`PROMPT_COMMAND` in Bash or in `precmd_functions` in Zsh.

Code is written in Hy and generated to Python3.
"


(eval-when-compile
  (require [hy.contrib.walk [let]]))

(import [terminatorlib.plugin :as plugin]
        ;; [terminatorlib.util [err dbg]]
        [terminatorlib.terminator [Terminator]])
(import gi)

(gi.require_version "Notify" "0.7")
(import [gi.repository [GObject GLib Notify]])



(setv VERSION "0.1.0")
(setv AVAILABLE ["LongCommandNotify"])


(defclass LongCommandNotify [plugin.Plugin]
  (setv capabilities ["command_watch"]
        watched #{})

  (defn __init__ [self]
        (.update-watched self)
        (.init Notify "Terminator"))

  (defn update-watched [self &rest _]
        "Updates the list of watched terminals"

        (let [new-watched #{}]
             (for [term (. (Terminator) terminals)]
                  (.add new-watched term)
                  (if-not (in term self.watched)
                          (let [vte (.get_vte term)]
                               (.connect term "focus-out" self.update-watched-delayed None)
                               (.connect vte "focus-out-event" self.update-watched-delayed None)
                               (.connect vte "notification-received" self.notification-received term))))
             (setv self.watched new-watched)))

  (defn update-watched-delayed [self &rest _]
        (GObject.idle_add (fn [self] (.update-watched self) False) self)
        True)

  (defn notification-received [self vte summary body terminator_term]
        (if (not (.has_focus vte))
            (-> (.new Notify.Notification summary body "terminator")
                (.show)))
        None))
