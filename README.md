## Goal

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


## Rust code

The [rust] code is a side-project, done outside of work, to continue learning the language and compare performance in a real-world project.

[rust]: <https://www.rust-lang.org/>

Principles for development:
- Python functionality will be implemented first.
- The rust code won't have core functionality that the python version doesn't have.

---


## Notes

- [pymarc documentation](https://gitlab.com/pymarc/pymarc)


--- 


## Logic

This [BruKnow webpage] for "Nostalgia : a novel", by Mircea Cărtărescu, shows a bookplate.

The MARC-record for this item is below.

It shows three elements that contain bookplate info:
- 996, subfields "u" and "z" -- only field relevant for bookplate-display
- 876, subfield "r" -- not relevant for bookplate-display
- there is also sometimes some bookplate info in the 945 field (not currently exported) -- not relevant for bookplate-display

So the initial script flow...

- From the daily "changes" MARC export, look for any records that contain bookplate info. 
    - Note: the changes causing these records to appear will most often not have anything to do with bookplates. 

For each record that contains bookplate info:

- See if the book-plate is already displaying in BruKnow. If so, move on to the next record. If not...

- Check the MySQL bookplate database to see if the expected data is in the relevant table.
    - If the expected data _is_ in the database, log this curiosity with a warning.
    - If the expected data is _not_ in the database, insert it, pause, and recheck BruKnow 

- Finally, email the relevant people any anomolies.

[BruKnow webpage]: <https://bruknow.library.brown.edu/permalink/01BU_INST/9mvq88/alma991003874639706966>

---


## Misc

"Nostalgia" MARC-record...

```
  <record>
    <leader>01226nam a2200313Ia 4500</leader>
    <controlfield tag="005">20080522191149.0</controlfield>
    <controlfield tag="008">050630s2005 nyu 000 1 eng</controlfield>
    <controlfield tag="001">991003874639706966</controlfield>
    <datafield tag="010" ind1="" ind2="">
      <subfield code="a">2005018927</subfield>
    </datafield>
    <datafield tag="020" ind1="" ind2="">
      <subfield code="a">0811215881 (alk. paper)</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">(RPB)b38928887-01bu_inst</subfield>
    </datafield>
    <datafield tag="035" ind1="" ind2="">
      <subfield code="a">(OCoLC)ocm60798481</subfield>
      <subfield code="9">ExL</subfield>
    </datafield>
    <datafield tag="040" ind1="" ind2="">
      <subfield code="a">DLC</subfield>
      <subfield code="c">DLC</subfield>
      <subfield code="d">DLC</subfield>
      <subfield code="d">NhCcYBP</subfield>
    </datafield>
    <datafield tag="041" ind1="1" ind2="">
      <subfield code="a">eng</subfield>
      <subfield code="h">rum</subfield>
    </datafield>
    <datafield tag="042" ind1="" ind2="">
      <subfield code="a">pcc</subfield>
    </datafield>
    <datafield tag="050" ind1="0" ind2="0">
      <subfield code="a">PC840.13.A86</subfield>
      <subfield code="b">N6713 2005</subfield>
    </datafield>
    <datafield tag="090" ind1="" ind2="">
      <subfield code="a">PC840.13.A86</subfield>
      <subfield code="b">N6713 2005</subfield>
    </datafield>
    <datafield tag="100" ind1="1" ind2="">
      <subfield code="a">Cărtărescu, Mircea.</subfield>
    </datafield>
    <datafield tag="245" ind1="1" ind2="0">
      <subfield code="a">Nostalgia :</subfield>
      <subfield code="b">a novel /</subfield>
      <subfield code="c">by Mircea Cărtărescu ; translated, with an afterword, from the Romanian by Julian Semilian ; introduction by Andrei Codrescu.</subfield>
    </datafield>
    <datafield tag="260" ind1="" ind2="">
      <subfield code="a">New York :</subfield>
      <subfield code="b">New Directions,</subfield>
      <subfield code="c">2005.</subfield>
    </datafield>
    <datafield tag="300" ind1="" ind2="">
      <subfield code="a">xiii, 322 p. ;</subfield>
      <subfield code="c">23 cm.</subfield>
    </datafield>
    <datafield tag="490" ind1="0" ind2="">
      <subfield code="a">New Directions paperbook ;</subfield>
      <subfield code="v">1018.</subfield>
    </datafield>
    <datafield tag="700" ind1="1" ind2="">
      <subfield code="a">Semilian, Julian.</subfield>
    </datafield>
    <datafield tag="907" ind1="" ind2="">
      <subfield code="a">.b38928887</subfield>
      <subfield code="b">06-18-15</subfield>
      <subfield code="c">12-19-05</subfield>
    </datafield>
    <datafield tag="998" ind1="" ind2="">
      <subfield code="a">r0001</subfield>
      <subfield code="b">12-19-05</subfield>
      <subfield code="c">m</subfield>
      <subfield code="d">a</subfield>
      <subfield code="e">-</subfield>
      <subfield code="f">eng</subfield>
      <subfield code="g">nyu</subfield>
      <subfield code="h">0</subfield>
      <subfield code="i">1</subfield>
    </datafield>
    <datafield tag="910" ind1="" ind2="">
      <subfield code="a">ybp</subfield>
    </datafield>
    <datafield tag="910" ind1="" ind2="">
      <subfield code="a">Backstage</subfield>
    </datafield>
    <datafield tag="910" ind1="" ind2="">
      <subfield code="a">Hathi Trust report SPM</subfield>
    </datafield>
    <datafield tag="993" ind1="" ind2="">
      <subfield code="a">ftp121905</subfield>
    </datafield>
    <datafield tag="996" ind1="" ind2="">
      <subfield code="u">http://library.brown.edu/bookplates/fund.php?account=EN464195</subfield>
      <subfield code="z">Purchased with the Fried Book Fund</subfield>
    </datafield>
    <datafield tag="900" ind1="0" ind2="">
      <subfield code="b">ROCK</subfield>
      <subfield code="d">STACKS</subfield>
      <subfield code="f">PC840.13.A86</subfield>
      <subfield code="f">N6713 2005</subfield>
      <subfield code="8">22261682420006966</subfield>
    </datafield>
    <datafield tag="876" ind1="" ind2="">
      <subfield code="ff">22261682420006966</subfield>
      <subfield code="u">0</subfield>
      <subfield code="j">0</subfield>
      <subfield code="aa">STACKS</subfield>
      <subfield code="t">BOOK</subfield>
      <subfield code="s">31236018603129</subfield>
      <subfield code="z">STACKS</subfield>
      <subfield code="a">23261682410006966</subfield>
      <subfield code="c">CIRCREG</subfield>
      <subfield code="bb">PC840.13.A86 N6713 2005</subfield>
      <subfield code="v">false</subfield>
      <subfield code="r">STAT_NOTE_2_FUND: bookplate EN464195_purchased_2006</subfield>
      <subfield code="h">ROCK</subfield>
      <subfield code="i">ROCK</subfield>
    </datafield>
  </record>
```