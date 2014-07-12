import csv
import os.path

offenses = []
ilcs_to_iucr = {}

class Offense(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __repr__(self):
        return "<Offense:{}>".format(str(self))

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
    offenses = []
    offenses_seen = set()
    ilcs_to_iucr = {}

    if filename is None:
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'data', 'ilcs2iucr.csv')

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['index_offense'] = row['index_offense'].upper() == "TRUE"
            row['csa_mvt_without_hierarchy'] = row['csa_mvt_without_hierarchy'].upper() == "TRUE"
            ilcs = row['ilcs_reference']
            offense = Offense(
                code=row['code'],
                offense=row['offense'],
                offense_category=row['offense_category'],
                index_offense=row['index_offense'],
                csa_mvt_without_hierarchy=row['csa_mvt_without_hierarchy']
            )

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

    return offenses, ilcs_to_iucr


def lookup_by_ilcs(chapter_or_reference, act_prefix=None, section=None):
    if act_prefix is None:
        # Only the first argument is specified,  That means it actually
        # represents an ilcs_reference
        ilcs_reference = chapter_or_reference
    elif chapter_or_reference and act_prefix and section:
        ilcs_reference = "{}-{}/{}".format(chapter_or_reference, act_prefix, section)
    else:
        raise TypeError("You must specify an ILCS reference or a chapter, "
                "act prefix and section")

    return ilcs_to_iucr[ilcs_reference]


offenses, ilcs_to_iucr = load_offenses()
