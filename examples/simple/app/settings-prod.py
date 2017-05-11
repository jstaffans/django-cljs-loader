from .settings import *
CLJS_LOADER = {
    # where to find the Leiningen project file
    'PROJECT_FILE': os.path.join(BASE_DIR, 'project.clj'),

    # If True, tries to load JS files from the Figwheel dev server.
    # Set to False in production mode.
    'FIGWHEEL': False,

    # which cljs build to use
    'CLJS_BUILD': Keyword('min'),

    # Which folder to use as the document root for assets built by Leiningen.
    #
    # In development mode, this should match the Figwheel root.
    #
    # In production mode, match the folder where cljsbuild outputs
    # its compiled JavaScript files, e.g. a 'dist' folder, which
    # is covered by one of the STATICFILES_DIRS above.
    'ROOT': 'assets/public/',
}
