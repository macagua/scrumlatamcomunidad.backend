from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import slc_sitioweb


class SLC_SITIOWEBLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=slc_sitioweb)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "slc_sitioweb:default")
        applyProfile(portal, "slc_sitioweb:initial")


SLC_SITIOWEB_FIXTURE = SLC_SITIOWEBLayer()


SLC_SITIOWEB_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SLC_SITIOWEB_FIXTURE,),
    name="SLC_SITIOWEBLayer:IntegrationTesting",
)


SLC_SITIOWEB_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SLC_SITIOWEB_FIXTURE, WSGI_SERVER_FIXTURE),
    name="SLC_SITIOWEBLayer:FunctionalTesting",
)


SLC_SITIOWEBACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SLC_SITIOWEB_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="SLC_SITIOWEBLayer:AcceptanceTesting",
)
