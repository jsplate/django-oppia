
from django.urls import reverse
from oppia.test import OppiaTestCase


class PermissionsViewTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def assert_response(self, view, status_code, user=None, view_kwargs=None):
        route = reverse(view, kwargs=view_kwargs)
        res = self.get_view(route, user)
        self.assertEqual(res.status_code, status_code)
        return res

    def assert_can_view(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 200, user, view_kwargs)

    def assert_cannot_view(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 401, user, view_kwargs)

    def assert_unauthorized(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 403, user, view_kwargs)

    def assert_must_login(self, view, user=None, view_kwargs=None):
        route = reverse(view, kwargs=view_kwargs)
        res = self.get_view(route, user)
        login_url = self.login_url + '?next=' + route
        self.assertRedirects(res, login_url)
        return res

    # upload media file
    def test_anon_cantview_av_upload(self):
        self.assert_must_login('av:upload')

    def test_admin_canview_av_upload(self):
        self.assert_can_view('av:upload', self.admin_user)

    def test_staff_canview_av_upload(self):
        self.assert_can_view('av:upload', self.staff_user)

    def test_student_cantview_av_upload(self):
        self.assert_unauthorized('av:upload', self.normal_user)

    def test_teacher_canview_av_upload(self):
        # since has can_upload set in profile
        self.assert_can_view('av:upload', self.teacher_user)
