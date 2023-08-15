"""Community Sponsor Content Type tests for this package."""
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from slc_web import ADD_SPONSOR_ROLES
from slc_web import MANAGE_SPONSOR_ROLES
from slc_web.testing import SLC_WEB_INTEGRATION_TESTING
from zope.component import queryUtility

import unittest


class CommunitySponsorContentTypeTest(unittest.TestCase):
    """The Community Sponsor Content Type Test class

    Args:
        unittest (class): unittest TestCase
    """

    layer = SLC_WEB_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _check_permission_for_role(self, permission, role):
        """Check if the specified role has the specified permission.
        The API of the permissionsOfRole() function sucks - it is bound too
        closely up in the permission management screen's user interface.

        Args:
            permission (str): permission string
            role (str): role string

        Returns:
            bool: True or False if permission in role
        """
        return permission in [
            r["name"] for r in self.portal.permissionsOfRole(role) if r["selected"]
        ]

    def test_ct_community_sponsor_fti(self):
        """Test If CommunitySponsor exits on Dexterity FTI."""
        fti = queryUtility(IDexterityFTI, name="CommunitySponsor")
        self.assertTrue(fti)
        # self.assertNotEqual(None, fti)

    def test_ct_community_sponsor_globally_addable(self):
        """Test If CommunitySponsor is globally addable."""

        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="CommunitySponsor")
        self.assertTrue(
            fti.global_allow,
            "{0} is not globally addable!".format(fti.id),
        )

    # profiles/default/rolemap.xml file
    def test_ct_community_sponsor_roles(self):
        """Test correct assigning of permissions registered."""

        # Test permission mapping for adding an Community Sponsor
        sponsor_roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(
                "Community Sponsor: Add Community Sponsor"
            )
            if r["selected"]
        ]
        self.assertEqual(sponsor_roles, ADD_SPONSOR_ROLES)

        # Test permission mapping for View Detail
        sponsor_roles = [
            r["name"]
            for r in self.portal.rolesOfPermission("Community Sponsor: View Detail")
            if r["selected"]
        ]
        self.assertEqual(sponsor_roles, MANAGE_SPONSOR_ROLES)

        # Test permission mapping for managing Manage Sponsors
        sponsor_roles = [
            r["name"]
            for r in self.portal.rolesOfPermission("Community Sponsor: Manage Sponsors")
            if r["selected"]
        ]
        self.assertEqual(sponsor_roles, MANAGE_SPONSOR_ROLES)

    # profiles/default/rolemap.xml file
    def test_ct_community_sponsor_manage_disabled(self):
        """Test that Community Sponsor is disabled."""
        self.assertFalse(
            self._check_permission_for_role(
                permission="Community Sponsor: Manage Sponsors",
                role="Member",
            )
        )

    # profiles/default/rolemap.xml file
    def test_ct_community_sponsor_manage_editable(self):
        """Test that 'Manager' and 'Sponsorship Committee'
        members can manage sponsors."""

        self.assertTrue(
            self._check_permission_for_role(
                permission="Community Sponsor: Manage Sponsors",
                role="Sponsorship Committee",
            )
        )
        self.assertTrue(
            self._check_permission_for_role(
                permission="Community Sponsor: Manage Sponsors",
                role="Manager",
            )
        )

    # profiles/default/rolemap.xml file
    def test_ct_community_sponsor_add_disabled(self):
        """Test that 'Member' role members does not add new sponsors."""
        self.assertFalse(
            self._check_permission_for_role(
                permission="Community Sponsor: Add Community Sponsor",
                role="Member",
            )
        )

    # profiles/default/rolemap.xml file
    def test_ct_community_sponsor_only_roles_can_add(self):
        """Test that only 'Sponsorship Committee' and 'Manager'
        members can add new sponsors."""
        self.assertTrue(
            self._check_permission_for_role(
                permission="Community Sponsor: Add Community Sponsor",
                role="Sponsorship Committee",
            )
        )
        self.assertTrue(
            self._check_permission_for_role(
                permission="Community Sponsor: Add Community Sponsor",
                role="Manager",
            )
        )
        # self.assertTrue(self._check_permission_for_role(
        #     permission='Community Sponsor: Add Community Sponsor',
        #     role='Site Administrator',
        # ))

    # profiles/default/rolemap.xml file
    def test_ct_community_sponsor_view_disabled(self):
        """Test that 'Member' and 'Anonymous' role members
        can sponsors view detail."""
        self.assertFalse(
            self._check_permission_for_role(
                permission="Community Sponsor: View Detail",
                role="Member",
            )
        )
        # self.assertFalse(
        #     self._check_permission_for_role(
        #         permission="Community Sponsor: View Detail",
        #         role="Anonymous",
        #     )
        # )

    # profiles/default/rolemap.xml file
    def test_ct_community_sponsor_view_only_roles_can_add(self):
        """Test that only 'Sponsorship Committee' and'Manager'
        members can sponsors view detail."""
        self.assertTrue(
            self._check_permission_for_role(
                permission="Community Sponsor: View Detail",
                role="Sponsorship Committee",
            )
        )
        self.assertTrue(
            self._check_permission_for_role(
                permission="Community Sponsor: View Detail",
                role="Manager",
            )
        )
        # self.assertTrue(self._check_permission_for_role(
        #     permission='Community Sponsor: View Detail',
        #     role='Site Administrator',
        # ))
