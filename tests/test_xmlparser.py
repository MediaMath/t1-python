import unittest
from terminalone.xmlparser import XMLParser, ParseError
from terminalone import errors


class TestXMLParsing(unittest.TestCase):
    def test_auth_error(self):
        with self.assertRaises(errors.AuthRequiredError) as cm:
            XMLParser(open('fixtures/auth_error.xml').read())
        exc = cm.exception
        self.assertEqual(exc.message, 'Authentication error')

    def test_developer_inactive(self):
        with self.assertRaises(errors.T1Error) as cm:
            XMLParser(open('fixtures/login_no_key.xml').read())
        exc = cm.exception
        self.assertEqual(exc.message, '<h1>Developer Inactive</h1>')

    def test_status_ok(self):
        parser = XMLParser(open('fixtures/session.xml').read())
        self.assertEqual(True, parser.status_code)

    def test_no_entities(self):
        parser = XMLParser(open('fixtures/no_entities.xml').read())
        self.assertEqual(True, parser.status_code)
        self.assertEqual(0, parser.entity_count)

    def test_one_entity(self):
        parser = XMLParser(open('fixtures/one_entity.xml').read())
        self.assertEqual(True, parser.status_code)
        self.assertEqual(1, parser.entity_count)

    def test_multiple_entities(self):
        parser = XMLParser(open('fixtures/three_entities.xml').read())
        self.assertEqual(True, parser.status_code)
        self.assertEqual(3, parser.entity_count)
