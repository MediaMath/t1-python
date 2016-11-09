import unittest
from terminalone.jsonparser import JSONParser
from terminalone import errors


class TestXMLParsing(unittest.TestCase):
    def test_auth_error(self):
        with open('tests/fixtures/auth_error.json') as f:
            fixture = f.read()
        with self.assertRaises(errors.AuthRequiredError) as cm:
            JSONParser(fixture)
        exc = cm.exception
        self.assertEqual(exc.message, 'Authentication error')

    def test_field_errors(self):
        with open('tests/fixtures/field_errors.json') as f:
            fixture = f.read()
        with self.assertRaises(errors.ValidationError) as cm:
            JSONParser(fixture)
        exc = cm.exception
        self.assertIn('Must supply advertiser_id', exc.message, )

    def test_status_ok(self):
        with open('tests/fixtures/session.json') as f:
            fixture = f.read()
        parser = JSONParser(fixture)

        self.assertEqual(True, parser.status_code)

    def test_no_entities(self):
        with open('tests/fixtures/no_entities.json') as f:
            fixture = f.read()
        parser = JSONParser(fixture)

        self.assertEqual(True, parser.status_code)
        self.assertEqual(0, parser.entity_count)

    def test_one_entity(self):
        with open('tests/fixtures/one_entity.json') as f:
            fixture = f.read()
        parser = JSONParser(fixture)

        self.assertEqual(True, parser.status_code)
        self.assertEqual(1, parser.entity_count)

    def test_multiple_entities(self):
        with open('tests/fixtures/three_entities.json') as f:
            fixture = f.read()

        parser = JSONParser(fixture)
        self.assertEqual(True, parser.status_code)
        self.assertEqual(3, parser.entity_count)
