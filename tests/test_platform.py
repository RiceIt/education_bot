from unittest import TestCase

from parser.platforms import FindAPhD
from parser.config import Configuration

Configuration.DEV = True


class FindAPhDTest(TestCase):
    def setUp(self) -> None:
        grant_soup = FindAPhD.get_grants_list()[0]
        self.find_a_phd = FindAPhD(grant_soup)

    def test_parse_title(self):
        self.find_a_phd.parse_title()
        self.assertEqual("Advanced Oxidation Processes using Light-Emitting Diodes for water treatment PhD",
                         self.find_a_phd.title)

