from unittest import TestCase

import iucr

class LookupTestCase(TestCase):
    def test_lookup_by_ilcs_reference(self):
        test_values = [
            ('720-5/9-1', '0110'),
        ]

        for ilcs_ref, iucr_code in test_values:
            iucr_obj = iucr.lookup_by_ilcs(ilcs_ref)[0]
            self.assertEqual(iucr_obj.code, iucr_code)

    def test_lookup_by_ilcs_bits(self):
        test_values = [
            ('720', '5', '9-1', '0110'),
        ]

        for chapter, act_prefix, section, iucr_code in test_values:
            iucr_obj = iucr.lookup_by_ilcs(chapter, act_prefix, section)[0]
            self.assertEqual(iucr_obj.code, iucr_code)

    def test_lookup_by_code(self):
        code = '0110'
        iucr_obj = iucr.lookup_by_code(code)
        self.assertEqual(iucr_obj.code, code)
