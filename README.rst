===========
python-iucr
===========

Python package for working with Illinois Uniform Crime Reporting (IUCR) data.

It's primary use case is as a crosswalk between Illinois Compiled Statutes (ILCS) reference and an Illinois Unified Crime Reporting (IUCR) code.

Installation
============

        pip install git+https://github.com/sc3/python-iucr.git

Features
========

Look up an IUCR offense by ILCS reference
-----------------------------------------

        >>> import iucr
        >>> offenses = iucr.lookup_by_ilcs("720-5/9-1")
        >>> print(offenses[0].code)
        0110
        >>> print(offenses[0].offense_category)
        Homicide
        >>> print(offenses[0].index_offense)
        True

You can also look up the IUCR offense based on the components (chapter, act prefix and section) of the ILCS code.


        >>> import iucr
        >>> offenses = iucr.lookup_by_ilcs("720", "5", "9-1")
        >>> print(offenses[0].code)
        0110
        >>> print(offenses[0].offense_category)
        Homicide
        >>> print(offenses[0].index_offense)
        True

Look up an IUCR offense by IUCR code
------------------------------------
        >>> import iucr
        >>> offense = iucr.lookup_by_code("0110")
        >>> print(offense.code)
        0110
        >>> print(offense.offense_category)
        Homicide
        >>> print(offense.index_offense)
        True

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
