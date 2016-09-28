from __future__ import absolute_import
from time import time
import unittest
from terminalone.models import campaign
from terminalone.models import strategy

API_BASE = 'api.mediamath.com'

expected_token = {
    'access_token': 'accesstoken',
    'expires_in': 3600,
    'refresh_token': 'refreshtoken',
    'token_type': 'Bearer',
}


def to_nearest_hundred(number):
    return round(float(number) / 100) * 100


def mock_saver(_):
    pass


class TestRemoveDeprecatedFields(unittest.TestCase):
    """Tests for removing deprecated fields on save from strategy and campaign entities"""

    def setUp(self):
        mock_campaign_properties = {
            "spend_cap_enabled": False,
            "spend_cap_type": "no-limit",
            "spend_cap_automatic": True

        }
        mock_strategy_properties = {
            "impression_pacing_interval": "day",
            "impression_pacing_type": "no-limit",
            "impression_pacing_amount": 10,
            "impression_cap": 10,

        }
        self.campaign = campaign.Campaign(None, mock_campaign_properties)
        self.strategy = strategy.Strategy(None, mock_strategy_properties)

    def test_campaign_remove_both_fields_when_no_changes(self):
        fields_to_remove = self.campaign._migration_asst()
        expected = ['spend_cap_enabled', 'spend_cap_type']
        self.assertEqual(expected, fields_to_remove)

    def test_campaign_remove_new_field_when_old_changed(self):
        self.campaign.spend_cap_enabled = True

        fields_to_remove = self.campaign._migration_asst()
        expected = ['spend_cap_type']
        self.assertEqual(expected, fields_to_remove)

    def test_campaign_remove_old_field_when_new_changed(self):
        self.campaign.spend_cap_type = 'derp'

        fields_to_remove = self.campaign._migration_asst()
        expected = ['spend_cap_enabled']
        self.assertEqual(expected, fields_to_remove)

    def test_campaign_remove_old_field_when_both_changed(self):
        self.campaign.spend_cap_type = 'derp'
        self.campaign.spend_cap_enabled = True

        fields_to_remove = self.campaign._migration_asst()
        expected = ['spend_cap_enabled']
        self.assertEqual(expected, fields_to_remove)

    def test_strategy_remove_all_fields_when_no_changes(self):
        fields_to_remove = self.strategy._migration_asst()
        expected = ['impression_pacing_interval', 'impression_pacing_type', 'impression_pacing_amount',
                    'impression_cap']
        self.assertItemsEqual(expected, fields_to_remove)

    def test_strategy_remove_new_fields_when_old_changed(self):
        self.strategy.impression_cap = 1

        fields_to_remove = self.strategy._migration_asst()
        expected = ['impression_pacing_interval', 'impression_pacing_type', 'impression_pacing_amount']
        self.assertItemsEqual(expected, fields_to_remove)

    def test_strategy_remove_old_fields_when_new_changed(self):
        self.strategy.impression_pacing_interval = 'derp'
        self.strategy.impression_pacing_type = 'derp'
        self.strategy.impression_pacing_amount = 1

        fields_to_remove = self.strategy._migration_asst()
        expected = ['impression_cap']
        self.assertItemsEqual(expected, fields_to_remove)

    def test_strategy_remove_old_fields_when_all_changed(self):
        self.strategy.impression_pacing_interval = 'derp'
        self.strategy.impression_pacing_type = 'derp'
        self.strategy.impression_pacing_amount = 1
        self.strategy.impression_cap = 1

        fields_to_remove = self.strategy._migration_asst()
        expected = ['impression_cap']
        self.assertItemsEqual(expected, fields_to_remove)
