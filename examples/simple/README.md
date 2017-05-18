Simple example of Django and ClojureScript integration with the
django-cljs library. 

## Usage

First set up a virtualenv and install the packages from `requirements.txt`.

### Development 

```shell
$> python manage.py migrate
$> python manage.py runserver
```

In another terminal window, do:

```shell
$> lein figwheel
```

Alternatively, start a Clojure REPL and run `(fig-start)` to start Figwheel compilation.

You can now visit http://localhost:8000 and see the [re-frame sample application][re-frame-sample]
running.

### Production

```shell
$> lein do clean, cljsbuild once min
$> python manage.py collectstatic
$> DJANGO_SETTINGS_MODULE=app.settings-prod python manage.py runserver
```

[re-frame-sample]: https://github.com/Day8/re-frame/tree/master/examples/simple
