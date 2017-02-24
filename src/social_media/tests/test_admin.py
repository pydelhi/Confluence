# coding=utf-8

from datetime import datetime
from unittest import mock

from django.contrib.admin.sites import AdminSite

from social_media.admin import PostAdmin
from social_media.models import Post
from registration.models import User


class MockUser(mock.Mock):
    """ Class to Mock User object."""

    def has_perm(self, perm):
        return True


class MockRequest(mock.Mock):
    """Class to Mock request object."""
    user = MockUser(spec=User)


class Dummy(mock.Mock):
    """Class to mock any object."""
    def set_attributes(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestPostAdmin:

    @classmethod
    def setup_post(self):
        """Should be called, whenever a fresh data is required to set."""
        self.post.set_attributes(
            text=None,
            photo=None,
            created_by=None,
            created_at=None,
            moderated_by=None,
            moderated_at=None,
            posted_at=None,
            platforms=None,
            status=None,
        )

    def setup_class(self):
        self.site = AdminSite()
        self.obj = mock.Mock()
        self.post_admin = PostAdmin(Post, self.site)
        self.request = mock.Mock()

        self.post = Dummy()
        self.setup_post()

    def setup_for_save_model(self):
        request = MockRequest()
        obj = self.post
        form = mock.Mock()
        change = mock.Mock()
        return request, obj, form, change

    def test_get_readonly_fields_for_accepted_posts(self):
        self.post.status = 'A'

        readonly_fields_for_accepted_post = self.post_admin.get_readonly_fields(self.request, self.post)
        assert readonly_fields_for_accepted_post == ('text', 'photo', 'platforms', 'status')

    def test_get_readonly_fields_for_non_accepted_posts(self):
        self.obj.status = 'Anything'

        readonly_fields_for_accepted_post = self.post_admin.get_readonly_fields(self.request, self.obj)
        assert readonly_fields_for_accepted_post == ()

    def test_set_attr_if_not_set_when_doesnt_have_attr(self):
        obj_with_no_attr_set = self.post
        self.post_admin.set_attr_if_not_set(obj_with_no_attr_set, 'created_by', 'foo')
        assert obj_with_no_attr_set.created_by == 'foo'

    def test_set_attr_if_not_set_when_attr_is_none(self):
        obj_with_attr_as_none = self.post
        obj_with_attr_as_none.foo = None
        self.post_admin.set_attr_if_not_set(obj_with_attr_as_none, 'created_at', 'bar')
        assert obj_with_attr_as_none.created_at == 'bar'

    def test_set_attr_if_not_set_when_attr_is_already_set(self):
        obj_with_attr_already_set = self.post
        obj_with_attr_already_set.foo = True
        self.post_admin.set_attr_if_not_set(obj_with_attr_already_set, 'foo', 'bar')
        assert obj_with_attr_already_set.foo != 'bar'

    def test_get_required_choices(self):
        choices, choices_not_required_set = ('A', 'B', 'C', 'D'), {'A', 'C'}
        required_choices = self.post_admin.get_required_choices(choices, choices_not_required_set)
        assert required_choices == ('B', 'D')

    def test_save_model_for_super_user(self):
        request, obj, form, change = self.setup_for_save_model()
        self.setup_post()
        request.user.is_superuser = True
        self.post_admin.save_model(request, obj, form, change)

        assert obj.moderated_by is request.user
        assert isinstance(obj.moderated_at, datetime)

    def test_save_model_for_normal_user(self):
        request, obj, form, change = self.setup_for_save_model()
        self.setup_post()
        request.user.is_superuser = False
        self.post_admin.save_model(request, obj, form, change)

        assert obj.created_by is request.user
        assert obj.status == 'H'
        assert isinstance(obj.created_at, datetime)
