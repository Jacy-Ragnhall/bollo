import copy

from django.template import Context
from django.test import SimpleTestCase


class TemplateContextCopyCompatibilityTests(SimpleTestCase):
    def test_context_copy_preserves_values_and_copies_the_dict_stack(self):
        context = Context({'value': 'original'})

        copied = copy.copy(context)

        self.assertIsInstance(copied, Context)
        self.assertEqual(copied['value'], 'original')
        self.assertIsNot(copied.dicts, context.dicts)
        self.assertEqual(copied.dicts, context.dicts)
