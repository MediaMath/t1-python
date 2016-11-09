import unittest
from terminalone.xmlparser import XMLParser
from terminalone import errors


class TestXMLParsing(unittest.TestCase):
    def test_auth_error(self):
        with open('tests/fixtures/xml/auth_error.xml') as f:
            fixture = f.read()
        with self.assertRaises(errors.AuthRequiredError) as cm:
            XMLParser(fixture)
        exc = cm.exception
        self.assertEqual(exc.message, 'Authentication error')

    def test_developer_inactive(self):
        with open('tests/fixtures/xml/login_no_key.xml') as f:
            fixture = f.read()
        with self.assertRaises(errors.T1Error) as cm:
            XMLParser(fixture)
        exc = cm.exception
        self.assertEqual(exc.message, '<h1>Developer Inactive</h1>')

    def test_status_ok(self):
        with open('tests/fixtures/xml/session.xml') as f:
            fixture = f.read()
        parser = XMLParser(fixture)

        self.assertEqual(True, parser.status_code)

    def test_no_entities(self):
        with open('tests/fixtures/xml/no_entities.xml') as f:
            fixture = f.read()
        parser = XMLParser(fixture)

        self.assertEqual(True, parser.status_code)
        self.assertEqual(0, parser.entity_count)

    def test_one_entity(self):
        with open('tests/fixtures/xml/one_entity.xml') as f:
            fixture = f.read()
        parser = XMLParser(fixture)

        self.assertEqual(True, parser.status_code)
        self.assertEqual(1, parser.entity_count)

    def test_multiple_entities(self):
        with open('tests/fixtures/xml/three_entities.xml') as f:
            fixture = f.read()

        parser = XMLParser(fixture)
        self.assertEqual(True, parser.status_code)
        self.assertEqual(3, parser.entity_count)
