django-cljs
===========

Transparent integration of ClojureScript in a Django project. Currently supports 
[Leiningen][] and [Figwheel][], which means you can rely on Figwheel's auto-refresh
features during development. 

This project is heavily inspired by the [django-webpack-loader][] project, which has the
similar goal of transparently including and using Webpack bundles in a Django project.

The integration with Leiningen is simplistic: information is read from the Leiningen
`project.clj` file to determine which output bundles are available and where. 
This means that there is a tight coupling to the structure of the Leiningen project
file -- expect things to break if you have a really exotic project setup!

## Install

```shell
$> pip install django-cljs
```

## Usage

### Examples

This repository contains one example application, have a look at that
to see a working setup in action.

* [Simple clock application][simple]

Some more advanced examples are on the way!

### Settings

Only Leiningen projects are supported. With a `project.clj` file somewhere
in your project, you can set the `django-cljs` loader up in your app settings.

It should look something like this:

```python
from edn_format.edn_lex import Keyword

BASE_DIR = ...  # should point to the project root

STATIC_URL = '/static/'

CLJS_LOADER = {
    # where to find the Leiningen project file
    'PROJECT_FILE': os.path.join(BASE_DIR, 'project.clj'),

    # If True, tries to load JS files from the Figwheel dev server.
    # Set to False in production mode.
    'FIGWHEEL': True,

    # Which cljs build (defined in the project.clj file) to use.
    # Change this for production.
    'CLJS_BUILD': Keyword('dev'),

    # The root folder for assets built by Leiningen.
    # In development mode, this matches the Figwheel root.
    'ROOT': 'assets/public',
}

# Add the folder where cljsbuild output lands as a source directory for the 
# staticfiles app. This assumes you are using the staticfiles app.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, CLJS_LOADER['ROOT']),
)

```

Where you put the ClojureScript source files is up to you - `assets/cljs` is
one possibility. See the example projects. 

### Template tag

Use the `render_bundle` template tag to hook the compiled ClojureScript bundle 
into your application. It will insert a `script` tag and call the `main` function
you have defined in the Leiningen project file.

```
{% load render_bundle from cljs_loader %}
...
<body>
  ...
  {% render_bundle %}  
</body>
```


### Development 

Open a second terminal and run `lein figwheel`. Alternatively, launch a REPL
and do `(fig-start)`. The JavaScript bundle will be loaded from the Figwheel
development server.

### Production

Assuming you have a cljsbuild profile called `prod`:

```
$> lein cljsbuild once prod
```

The compiled bundle that is produced by `lein cljsbuild` can be collected with 
`python manage.py collectstatic`, or whichever your preferred method of 
including production assets is.

The `render_bundle` template tag does not need to change.

## Contributing

You can run the test suite in the `tests` folder with the following command:


```
$> make test
```


[Leiningen]: http://leiningen.org/
[Figwheel]: https://github.com/bhauman/lein-figwheel
[django-webpack-loader]: https://github.com/owais/django-webpack-loader
[simple]: examples/simple


