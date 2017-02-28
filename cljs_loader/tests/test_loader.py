from django.test import TestCase
from cljs_loader import loader

class LoaderTestCase(TestCase):


    def test_config_as_vector(self):
        with self.settings(CLJS_LOADER={
                'PROJECT_FILE': 'cljs_loader/tests/project1.clj',
                'FIGWHEEL_ROOT': 'assets/public/'
        }):
            bundles = loader.Loader().get_bundles()
            self.assertDictEqual(bundles, {
                'dev': 'http://localhost:3449/out/frontend.js',
                'min': 'http://localhost:3449/out/frontend-min.js'
            })


    def test_config_as_map(self):
        with self.settings(CLJS_LOADER={
                'PROJECT_FILE': 'cljs_loader/tests/project2.clj',
                'FIGWHEEL_ROOT': 'assets/public/'
        }):
            bundles = loader.Loader().get_bundles()
            self.assertDictEqual(bundles, {
                'dev': 'http://localhost:3000/out/frontend2.js',
                'min': 'http://localhost:3000/out/frontend2-min.js'
            })
