from django.test import SimpleTestCase
from django.urls import resolve

from apps.jobs.views import admin_jobs_approval_list


class AdminApprovalRouteTests(SimpleTestCase):
    def test_admin_approvals_route_resolves_to_job_moderation_view(self):
        match = resolve('/admin/approvals/')

        self.assertEqual(match.func, admin_jobs_approval_list)
