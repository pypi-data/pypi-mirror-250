"""
Search Evaluate Action, © 2016 by Simon Arjuna Erat
---------------------------------------------------

SEA's Complex Data Structure Class (CDSC)
~~ a python dataclass experiment ~~

Abstract:
First part of the class is an enum which limits the "top level" count.
We then have a 3 dimensional array offering various "knot"s "node"s.

Within this 3 dimensional array, everything is a node! Everything has get/set.
Each node must have 1 parent. (a node can have any node as parent, but only one.)
Each node may have one or more children. (other nodes, making this one a knot - for explaning purposes)
Each node must have a node_label
Each node must have a node_type (1 of 3, --> double array, node based tree structure)
Each node might have a value
Each node might have a value_type (as example: str, int, bool, hex, float)
Each node might have content
Each node might have a message

And when I say "x dimensional array", i mean asociated arrays, well "array_name["My House"]".

For the 'structure' of the data, coding wise:
class.
	reload(str_import_db=None, bSafe=False) 	# Re-reads the file, without safing first, then refresh the tree (root)
	save(str_backup_db=None)					# Safe class.settings.filename or export it
	refresh(bVerbose=self.settings.bVerbose)	# Refresh while giving output to console, remove everything below class.<content of root_label>
class.settings. # (each have get/set property)
	bVerbose: bool
	filename: str
	title: str
	description: str
	logfile: str
	confile: str
	save(str_export_conf_file=None)		# Saves everything of class.settings.* (for example incl: class.settings.data.*)
	reload(str_import_conf_file=None, bSafe=False)
class.settings.data.  # The "enum list" is used for top level entries, and to define filenames for the seperate saving/loading. (also: set/get)
	enum: str, list
	prefix: str
	suffix: str
	ext: str
	root_label: str
class.query.
	list(enum,a,b,c)
	search(enum, str)
class.<root_label>.
	Enum1.
		<content of db>, use node parent/children attributes to structure it accordingly.
	Enum2.
		...
		

	
Example Usage:
say: class.settings.data.global is "global"
class.global.EntryOfSettings-Data-Enum.type = 1 # Being "double asociated array"
class.global.EntryOfSettings-Data-Enum[topic][section] = 2 # Beeing "nodes" (optimized for tree or other structures)
class.global.EntryOfSettings-Data-Enum.topic.section.type = 2 	# Later one... would do the same, type refering to node_type - in both meanings

this_list = class.query.list(enum,a,b,c)
this_string = class.query.search(enum, str)
	

important:
what would be the file size of an empty db?
what would be the memory (ram) footprint of the empty db while loaded / open?
In other words, what about would be the so called "overhead"?

"""
