


******

Bravo!  You have received a Medical Diploma from International Waters University.

******


# mergers

---

## description
This is a module that can reliably
ascertain the health status of software.

(It's like a testing kit)
		
---		
		
## install
`[ZSH] pip install mergers`

---
	
## documentation (this opens a server process that sends HTML)
`[ZSH] mergers shares`
	
---	
	
## internal status tests of the module
`[ZSH] mergers mergers`
	
	These checks are run with pypi "body_scan"
	"mergers" is built from a fork of "body_scan"
	("body_scan" checks are written with "unittest")
	
---

## status checks (tests)
- Checks are started simultaneously, unless "--simultaneous no"</p>
	
### Create a status file (glob pattern *_status.py).
(The glob pattern can be modified with the progammatic python3 interface)
```		
	# status_1.py
	
	def check_1 ():
		print ("check 1")
		
	def check_2 ():
		print ("check 2")
		
	def check_3 ():
		raise Exception ("not 110%")

	checks = {
		"check 1": check_1,
		"check 2": check_2,
		"check 3": check_3
	}
```
		
### from a directory deeper than the status file "status_1.py"
`[ZSH] mergers status`


#### The report then should appear like this
```
paths: [
	{
		"path": "../status_1.py",
		"empty": false,
		"parsed": true,
		"stats": {
			"passes": 2,
			"alarms": 1
		},
		"checks": [
			{
				"check": "check 1",
				"passed": true,
				"elapsed": [
					4.054199962411076e-05,
					"seconds"
				]
			},
			{
				"check": "check 2",
				"passed": true,
				"elapsed": [
					1.72930003827787e-05,
					"seconds"
				]
			},
			{
				"check": "check 3",
				"passed": false,
				"exception": "Exception('not 110%')",
				"exception trace": [
					"Traceback (most recent call last):",
					"  File \"/home/veganecology/.local/lib/python3.11/site-packages/mergers/processes/scan/process/keg/check.py\", line 68, in start",
					"    checks [ check ] ()",
					"  File \"<string>\", line 13, in check_3",
					"Exception: not 110%"
				]
			}
		]
	}
]
alarms: [
	{
		"path": "../status_1.py",
		"checks": [
			{
				"check": "check 3",
				"passed": false,
				"exception": "Exception('not 110%')",
				"exception trace": [
					"Traceback (most recent call last):",
					"  File \"/home/veganecology/.local/lib/python3.11/site-packages/mergers/processes/scan/process/keg/check.py\", line 68, in start",
					"    checks [ check ] ()",
					"  File \"<string>\", line 13, in check_3",
					"Exception: not 110%"
				]
			}
		]
	}
]
stats: {
	"alarms": 0,
	"empty": 0,
	"checks": {
		"passes": 2,
		"alarms": 1
	}
}
```
	
--

## advanced configurations
It's recommended to run mergers programmatilly.
An example of this can be found in the "advanced configurations"
section of the documentation.

## Contacts
bgrace2468@pm.me
	
</pre>
		
		
	