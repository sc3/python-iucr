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
        # Test values are in the format:
        # chapter, act_prefix, section, subsection_bits, expected code
        test_values = [
        
            # 720-5/9-1
            ('720', '5', '9-1', (), '0110'),
            # 720 ILCS 5 12-3.2(a)(1)
            ('720', '5', '12-3.2', ('a', '1'), '0486'),
            # 720 ILCS 570 402(c)
            ('720', '570', '402', ('c',), '2020'),
            # 720 ILCS 570 401(a)(1)(A)
            ('720', '570', '401', ('a', '1', 'A'), '2010'),
            # 720-550/4(a)(1)
            ('720', '550', '4', ('a', '1'), '1811'),
            
            # Not in crosswalk:
            # 625 ILCS 5 4-103.2(a)(7)(A)
            # ('625', '5', '4-103.2', ('a', '7', 'A'), )
        ]

        for chapter, act_prefix, section, section_bits, iucr_code in test_values:
            iucr_obj = iucr.lookup_by_ilcs(chapter, act_prefix, section, *section_bits)[0]
            self.assertEqual(iucr_obj.code, iucr_code)

    def test_lookup_by_code(self):
        code = '0110'
        iucr_obj = iucr.lookup_by_code(code)
        self.assertEqual(iucr_obj.code, code)
