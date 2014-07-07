from unittest import TestCase

import iucr

class LookupTestCase(TestCase):
    def test_lookup_by_ilcs(self):
        test_values = [
            ('720-5/9-1', '0110'),
        ]

        for ilcs_ref, iucr_code in test_values:
            iucr_obj = iucr.lookup_by_ilcs(ilcs_ref)[0]
            self.assertEqual(iucr_obj.code, iucr_code)
