# Goal

High-level goal:
- Bookplates show up in BruKnow after person updates MARC record

Specific sprint goal:
- For new MARC bookplate info -- update DB and ensure, then, that bookplate shows up in BruKnow.

Goals of "report" script...
- detect new MARC entries (updated since 2023-01-01?)
	- ensure there's a BruKnow entry
	- ensure there's a proper db entry
	- detect pattern(s) for success in the form of MARC-tests and db-tests
	- output report of MARC bookplate entries with no BruKnow bookplate
		- for each of these entries:
			- ascertain if problem is in MARC
			- ascertain if problem is in DB (could be both)
			
Goal of "ongoing" script...
- detect new MARC entries in the last month
- see if there is a BruKnow entry, if not...
- update bookplate-table(s)
- confirm there is a BruKnow bookplate
- alert designated people with errors

Brainstorming coolness...
- have ongoing script update a google-sheet "report"
- on a monthly basis summarize the spreadsheet in an email to folk

---
