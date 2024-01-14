





******

Bravo!  You have received a Medical Diploma in Shares from   
the Orbital Convergence University International Air and Water Embassy of the Tangerine Planet.  

You are now officially certified to include "shares" in your practice.

******


# shares

---

## description
Started from the shell, "shares" presents files in the current working directory (cwd) that have extension ".s.HTML" (case sensitive).

---		
		
## install
`[ZSH] pip install shares`

---


## start from shell
`[ZSH] shares`

Shares starts on port 2468, or the first avaible port after that.  
 * Running on http://127.0.0.1:2468  

### This is an example ".s.HTML" file:
```
<pre>
	<h1>This is an example html file.</h1>
	<p>It really only needs the "pre" tag to look like a reflection of its contents in a browser.</p>
	<p>Tags like "html" and "body" are actually not necessary for rendering HTML in modern browsers.</p>

	<p>for text to wrap, instead of extending off the page, style "white-space: pre-wrap" can be utilized.</p>
</pre>
---


## start programmatically
```
import pathlib
from os.path import dirname, join, normpath
this_folder = pathlib.Path (__file__).parent.resolve ()

import shares
shares.start ({
	"extension": ".s.HTML",
	
	#
	#	This is the node from which the traversal occur.
	#
	"directory": str (this_folder) + "/structures/shares",
	
	#
	#	This path is removed from the absolute path of share files found.
	#
	"relative path": str (this_folder) + "/structures/shares"
})
```