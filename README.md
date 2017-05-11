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

This repository contains two example applications, have a look at those
to see a working setup in action.

* [Simple clock application][simple]
* [Shopping cart application][cart]

### Settings

Only Leiningen projects are supported. With a `project.clj` file somewhere
in your project, you can set the `django-cljs` loader up in your app settings.
It should look something like this:

```python
from edn_format.edn_lex import Keyword

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets/public'),
)

CLJS_LOADER = {
    # where to find the Leiningen project file
    'PROJECT_FILE': os.path.join(BASE_DIR, 'project.clj'),

    # If True, tries to load JS files from the Figwheel dev server.
    # Set to False in production mode.
    'FIGWHEEL': True,

    # Which cljs build (defined in the project.clj file) to use.
    # you will want to change this for production.
    'CLJS_BUILD': Keyword('dev'),

    # Which folder to use as the document root for assets built by Leiningen.
    #
    # In development mode, this should match the Figwheel root.
    #
    # In production mode, match the folder where cljsbuild outputs
    # its compiled JavaScript files, e.g. a 'dist' folder, which
    # is covered by one of the STATICFILES_DIRS above.
    'ROOT': 'assets/public/',
}

```

### Template tag


```
{% load render_bundle from cljs_loader %}
...
<body>
  ...
  {% render_bundle %}  
</body>
```


### Development 



### Production


## Contributing

You can run the test suite in the `tests` folder with the following command:


```
$> make test
```


[Leiningen]: http://leiningen.org/
[Figwheel]: https://github.com/bhauman/lein-figwheel
[django-webpack-loader]: https://github.com/owais/django-webpack-loader
[simple]: examples/simple
[cart]: examples/shopping-cart


