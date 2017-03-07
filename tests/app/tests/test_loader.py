from django.test import TestCase
from cljs_loader import loader

class LoaderFigwheelTestCase(TestCase):

    def test_config_as_vector(self):
        with self.settings(CLJS_LOADER={
                'PROJECT_FILE': 'project1.clj',
                'ROOT': 'assets/public/out/',
                'FIGWHEEL': True
        }):
            bundles = loader.Loader().get_bundles()
            self.assertDictEqual(bundles, {
                'dev': {
                    'url': 'http://localhost:3449/frontend.js',
                    'on-jsload': 'frontend.core.run()'
                },
                'min': {
                    'url': 'http://localhost:3449/frontend-min.js',
                    'on-jsload': 'frontend.core.main()'
                },

            })


    def test_config_as_map(self):
        with self.settings(CLJS_LOADER={
                'PROJECT_FILE': 'project2.clj',
                'ROOT': 'assets/public/out/',
                'FIGWHEEL': True
        }):
            bundles = loader.Loader().get_bundles()
            self.assertDictEqual(bundles, {
                'dev': {
                    'url': 'http://localhost:3000/frontend2.js',
                    'on-jsload': 'frontend.core.run()'
                },
                'min': {
                    'url': 'http://localhost:3000/frontend2-min.js',
                    'on-jsload': 'frontend.core.main()'
                }
            })


class LoaderStaticTestCase(TestCase):

    def test_config_as_vector(self):
        with self.settings(
                STATIC_URL='/static/',
                CLJS_LOADER={
                    'PROJECT_FILE': 'project1.clj',
                    'ROOT': 'assets/public/out/',
                    'FIGWHEEL': False
                }):
            bundles = loader.Loader().get_bundles()
            self.assertDictEqual(bundles, {
                'dev': {
                    'url': '/static/frontend.js',
                    'on-jsload': 'frontend.core.run()'
                },
                'min': {
                    'url': '/static/frontend-min.js',
                    'on-jsload': 'frontend.core.main()'
                },

            })


    def test_config_as_map(self):
        with self.settings(
                STATIC_URL='/static/',
                CLJS_LOADER={
                    'PROJECT_FILE': 'project2.clj',
                    'ROOT': 'assets/public/out/',
                    'FIGWHEEL': False
                }):
            bundles = loader.Loader().get_bundles()
            self.assertDictEqual(bundles, {
                'dev': {
                    'url': '/static/frontend2.js',
                    'on-jsload': 'frontend.core.run()'
                },
                'min': {
                    'url': '/static/frontend2-min.js',
                    'on-jsload': 'frontend.core.main()'
                }
            })
