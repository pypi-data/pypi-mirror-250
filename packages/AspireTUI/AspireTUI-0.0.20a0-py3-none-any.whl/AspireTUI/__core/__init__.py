"""
Description: \n
	Hello Random Coder. \n
	Here you'll find everything eventhough you're not supposed to. \n
	\n
	This is the "Core Engine" if you will. \n
\n
======================================================== \n
File Created on:		2024 Jan. 11 \n
File Created by:		Simon Arjuna Erat \n
License:				MIT \n
URL:					https://www.github.com/sri-arjuna/ASPIRE \n
Based on my TUI & SWARM for the BASH shell © 2011 \n
"""

from AspireTUI.strings import now
from AspireTUI.Classes import _Log
from AspireTUI import _settings_self
_log = _Log.Log( _settings_self["log_conf"] )
_log.Settings.Title = f"Created with: AspireTUI (TODO VER), {now}"
_log.DEBUG("Logging Enabled")
