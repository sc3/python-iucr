"""Metadata for Illinois Unified Crime Reporting (IUCR) offenses."""
import csv
import os.path

__all__ = ['Offense', 'lookup_by_ilcs', 'lookup_by_code']

offenses = []
ilcs_to_iucr = {}
offenses_by_code = {}

class Offense(object):
    """
    A criminal offense that is part of the Illinois Uniform Crim Reporting
    (IUCR).

    Args:
        code (str): 4-digit IUCR code.
        offense (str): Human-readable description of the offense.
        offense_category (str): Category of the offense.
        index_offense (boolean): Whether the offense is an index offense.
        csa_mvt_without_hierarchy (boolean): Whether the offense is a
            Criminal Sexual Assault (CSA) or Motor Vehicle Theft (MVT)
            without the hiearchy rule applied.

    Attributes:
        code (str): 4-digit IUCR code.
        offense (str): Human-readable description of the offense.
        offense_category (str): Category of the offense.
        index_offense (boolean): Whether the offense is an index offense.
        csa_mvt_without_hierarchy (boolean): Whether the offense is a
            Criminal Sexual Assault (CSA) or Motor Vehicle Theft (MVT)
            without the hiearchy rule applied.

    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __repr__(self):
        return "<Offense: {}>".format(str(self))

    def __str__(self):
        return self.code

    def __hash__(self):
        return hash(self.code)

    def __lt__(self, other):
        return self.code < other.code

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.code > other.code 

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)


def load_offenses(filename=None):
    """
    Populate a list of offenses and the ILCS to IUCR crosswalk

    Args:
        filename (str): Filename of CSV file containing offenses.
           Defaults to ``{package_dir}/data/ilcs2iucr.csv``.
    
    Returns:
        Tuple where the first value is a list of Offense objects, 
        the second value is a dictionary mapping ILCS reference
        strings to Offense objects, and the third value is a
        dictionary mapping IUCR code to Offense objects.

    """
    offenses = []
    offenses_seen = set()
    ilcs_to_iucr = {}
    offenses_by_code = {}

    if filename is None:
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'data', 'ilcs2iucr.csv')

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['index_offense'] = row['index_offense'].upper() == "TRUE"
            row['csa_mvt_without_hierarchy'] = row['csa_mvt_without_hierarchy'].upper() == "TRUE"
            offense = Offense(
                code=row['code'],
                offense=row['offense'],
                offense_category=row['offense_category'],
                index_offense=row['index_offense'],
                csa_mvt_without_hierarchy=row['csa_mvt_without_hierarchy']
            )

            ilcs = row['ilcs_reference'].lower()
            if ilcs:
                try:
                    ilcs_offenses = ilcs_to_iucr[ilcs]
                    if offense not in ilcs_offenses:
                        ilcs_offenses.append(offense)
                except KeyError:
                    ilcs_to_iucr[ilcs] = [offense,]

            if offense not in offenses_seen:
                offenses.append(offense)
                offenses_seen.add(offense)

            offenses_by_code[offense.code] = offense

    return offenses, ilcs_to_iucr, offenses_by_code


def lookup_by_ilcs(chapter_or_reference, act_prefix=None, section=None,
        *subsection_bits):
    """
    Lookup an Illinois Unified Crime Reporting (IUCR) offense based on
    a section of the Illinois Compiled Statutes (ILCS).

    Args:
        chapter_or_reference (str): Either a full reference to an ILCS
           section, such as "720-5/7-1" or, if specifying the individual
           components, the chapter number.
        act_prefix (str): If specifying the individual components, the
            ILCS section's act prefix number.
        section (str): If specifying the individual component's the
            ILCS section's section number within the chapter and act.
        section_bits: Unlimited number of subsection or paragraph identifiers.

    Returns:
        Offense object matching the ILCS reference or section number
        components.

    Raises:
        KeyError if an offense matching the ILCS section is not found.

    """
    if act_prefix is None:
        # Only the first argument is specified,  That means it actually
        # represents an ilcs_reference
        ilcs_reference = chapter_or_reference
    elif chapter_or_reference and act_prefix and section:
        ilcs_reference = "{}-{}/{}".format(chapter_or_reference, act_prefix, section)
        for bit in subsection_bits:
            ilcs_reference += '({})'.format(bit)
    else:
        raise TypeError("You must specify an ILCS reference or a chapter, "
                "act prefix and section")

    try:
        return ilcs_to_iucr[ilcs_reference.lower()]
    except KeyError:
        # backoff by subsection, recursively; stop when subsection_bits is empty 
        if any(subsection_bits):
            return lookup_by_ilcs(chapter_or_reference, act_prefix, section, *subsection_bits[:-1])
        else:
            raise

def lookup_by_code(code):
    """
    Lookup an offense by its IUCR code.

    Args:
        code (str): 4-digit IUCR code.

    Returns:
        Offense object with specified IUCR code.

    Raises:
        KeyError if an offense matching the specified code is not found.

    """
    return offenses_by_code[code] 


offenses, ilcs_to_iucr, offenses_by_code = load_offenses()
