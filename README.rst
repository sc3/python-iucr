===========
python-iucr
===========

Python package for working with Illinois Uniform Crime Reporting (IUCR) data. 

About the data
==============

The data that drives this package is based on the crosswalk PDF found at https://www.isp.state.il.us/docs/6-260.pdf

It was manually extracted to a CSV file that can be found in ``data/ilcs2iucr.csv``.

One major data transformation that I performed was breaking out the asterisk that denotes an index offense into a separate field.  I also broke out the "(I)" that denotes a Criminal Sexual Assault (CSA) or Motor Vehicle Theft (MVT) without application of the hierarchy into a separate field.

Also, while the PDF defines ranges or comma-separated values when multiple ILCS references map to the same IUCR code, I created multiple rows.

Fields
------

* code: IUCR code
* offense: Description of offense
* ilcs_reference: Illinois Compiled Statutes (ILCS) Reference.  See https://www.isp.state.il.us/docs/IUCRoffcode0510.pdf
* us_code: United States Code Reference
* usmj_act: United States Code of Military Justice (USMJ) act number
* offense_category: General category of offense, as defined by the Illinois State Police
* index_offense: "TRUE" if the offense is an index offense  
* csa_mvt_without_hierarchy: "TRUE" if the offense s a Criminal Sexual Assault (CSA) and Motor Vehicle Theft (MVT) Without the Application of the Hierarchy Rule
