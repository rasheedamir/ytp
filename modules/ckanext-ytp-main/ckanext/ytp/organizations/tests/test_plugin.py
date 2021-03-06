# -*- coding: utf-8 -*-

import paste.fixture
import pylons.test
import simplejson

from ckan.tests import TestCase
from ckan.logic import NotFound
from ckan import tests, model, plugins
from ckan.lib.munge import munge_title_to_name
from ckanext.ytp.organizations.tests import tools
from ckanext.ytp.organizations.tasks import organization_import


class TestYtpOrganizationPlugin(TestCase):
    """ Test YtpOrganizationPlugin class """

    @classmethod
    def setup_class(cls):
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)

    def setup(self):
        self.sysadmin = model.User(name='test_sysadmin', sysadmin=True)
        model.Session.add(self.sysadmin)
        model.Session.commit()
        model.Session.remove()

    def teardown(self):
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        pass

    def test_create_unique_organizations(self):
        """ Test duplicate title name """
        tests.call_action_api(self.app, 'organization_create', name='test-name-1',
                              title="test-title", apikey=self.sysadmin.apikey)
        tests.call_action_api(self.app, 'organization_create', status=409, name='test-name-2',
                              title="test-title", apikey=self.sysadmin.apikey)

    def _create_context(self):
        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        admin_user = plugins.toolkit.get_action('get_site_user')(context, None)
        context['user'] = admin_user['name']
        return context

    def test_user_create_hook(self):
        self.assert_raises(NotFound, plugins.toolkit.get_action('organization_show'), self._create_context(), {"id": "yksityishenkilo"})

        plugins.toolkit.get_action('user_create')(self._create_context(), {"name": "test_create_1", "id": "test_create_1",
                                                                           "email": "example1@localhost", "password": "test_password",
                                                                           "fullname": "test_fullname_1"})
        plugins.toolkit.get_action('user_create')(self._create_context(), {"name": "test_create_2", "id": "test_create_2",
                                                                           "email": "example2@localhost", "password": "test_password",
                                                                           "fullname": "test_fullname_2"})
        plugins.toolkit.get_action('user_update')(self._create_context(), {"id": "test_create_2", "id": "test_create_2",
                                                                           "email": "example3@localhost", "password": "test_password",
                                                                           "fullname": "test_fullname_3"})

    def test_organization_import(self):
        """ Test organization import """
        organization_url = tools.get_organization_test_source()
        data = simplejson.dumps({'url': organization_url, 'public_organization': True})
        for _ in xrange(2):
            result = organization_import.apply((data,))
            self.assert_true(result.successful())
            for title in u"Kainuun ty\u00f6- ja elinkeinotoimisto", u"Lapin ty\u00f6- ja elinkeinotoimisto", u"Suomen ymp\u00e4rist\u00f6keskus":
                organization = tests.call_action_api(self.app, 'organization_show', id=munge_title_to_name(title).lower())
                self.assert_equal(organization['title'], title)
                public_org = 'false'
                for extra in organization['extras']:
                    if extra['key'] == 'public_adminstration_organization':
                        public_org = 'true'
                self.assert_equal(public_org, 'true')

    def test_organization_import_update(self):
        """ Test updating organization import from file """
        organization_url = tools.get_organization_test_source()

        for extras in False, True:
            data = {'url': organization_url}
            if extras:
                data['public_organization'] = True
            result = organization_import.apply((simplejson.dumps(data),))
            self.assert_true(result.successful())
            for title in u"Kainuun ty\u00f6- ja elinkeinotoimisto", u"Lapin ty\u00f6- ja elinkeinotoimisto", u"Suomen ymp\u00e4rist\u00f6keskus":
                organization = tests.call_action_api(self.app, 'organization_show', id=munge_title_to_name(title).lower())
                self.assert_equal(organization['title'], title)
                self.assert_true('public_adminstration_organization' not in organization)  # We do not want this to be updated

    def test_organization_import_with_name(self):
        """ Test organization import """
        expected = (u"hri", u"Ulkoinen lähde: Hri.fi", u"Tähän organisaatioon harvestoidaan tietoaineistoja Helsinki Region Infosharesta."), \
                   (u"datagovuk", u"Data.Gov.UK", u"")
        organization_url = tools.get_organization_harvest_test_source()
        data = simplejson.dumps({'url': organization_url})
        for _ in xrange(2):
            result = organization_import.apply((data,))
            self.assert_true(result.successful())
            for name, title, description in expected:
                organization = tests.call_action_api(self.app, 'organization_show', id=name)
                self.assert_equal(organization['title'], title)
                self.assert_equal(organization['description'], description)
                self.assert_true('public_adminstration_organization' not in organization)
