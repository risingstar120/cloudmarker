"""Tests for AzKVSecretNoExpiryEvent plugin."""


import copy
import unittest

from cloudmarker.events import azkvsecretnoexpiryevent

base_record = {
    'com':  {
        'cloud_type':  'azure',
        'record_type': 'key_vault_secret'
    },
    'ext': {
        'record_type': 'key_vault_secret',
        'enabled': True,
        'expiry_set': False
    }
}


class AzKVKeyNoExpiryEventTest(unittest.TestCase):
    """Tests for AzKVSecretNoExpiryEvent plugin."""

    def test_secret_bucket_missing(self):
        record = copy.deepcopy(base_record)
        record['com'] = None
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(events, [])

    def test_com_bucket_cloud_type_non_azure(self):
        record = copy.deepcopy(base_record)
        record['com']['cloud_type'] = 'non_azure'
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(events, [])

    def test_ext_bucket_missing(self):
        record = copy.deepcopy(base_record)
        record['ext'] = None
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(events, [])

    def test_secret_bucket_record_type_non_key_vault_key(self):
        record = copy.deepcopy(base_record)
        record['ext']['record_type'] = 'non_key_vault_key'
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(events, [])

    def test_secret_not_enabled_expiry_not_set(self):
        record = copy.deepcopy(base_record)
        record['ext']['enabled'] = False
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(events, [])

    def test_secret_not_enabled_and_expiry_set(self):
        record = copy.deepcopy(base_record)
        record['ext']['enabled'] = False
        record['ext']['expiry_set'] = True
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(events, [])

    def test_secret_enabled_and_expiry_set(self):
        record = copy.deepcopy(base_record)
        record['ext']['enabled'] = True
        record['ext']['expiry_set'] = True
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(events, [])

    def test_secret_enabled_and_expiry_notset(self):
        record = copy.deepcopy(base_record)
        plugin = azkvsecretnoexpiryevent. \
            AzKVSecretNoExpiryEvent()
        events = list(plugin.eval(record))
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['ext']['record_type'],
                         'key_vault_secret_no_expiry_event')
        self.assertEqual(events[0]['com']['record_type'],
                         'key_vault_secret_no_expiry_event')
        self.assertEqual(events[0]['com']['cloud_type'], 'azure')
