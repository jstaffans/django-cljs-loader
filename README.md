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

WIP

## Usage

### Development 

WIP

### Production

WIP

## Development 

You can run the test suite in the `tests` folder with the following command:


```
$> make test
```


[Leiningen]: http://leiningen.org/
[Figwheel]: https://github.com/bhauman/lein-figwheel
[django-webpack-loader]: https://github.com/owais/django-webpack-loader


