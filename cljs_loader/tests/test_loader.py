from django.test import TestCase
from cljs_loader import loader

class LoaderTestCase(TestCase):


    def test_config_as_vector(self):
        with self.settings(CLJS_LOADER={'PROJECT_FILE': 'cljs_loader/tests/project1.clj'}):
            bundles = loader.get_bundles()
            self.assertDictEqual(bundles, {
                'dev': 'out/frontend.js',
                'min': 'out/frontend-min.js'
            })


    def test_config_as_map(self):
        with self.settings(CLJS_LOADER={'PROJECT_FILE': 'cljs_loader/tests/project2.clj'}):
            bundles = loader.get_bundles()
            self.assertDictEqual(bundles, {
                'dev': 'out/frontend2.js',
                'min': 'out/frontend2-min.js'
            })
