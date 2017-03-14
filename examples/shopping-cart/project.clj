(defproject frontend "0.1.0-SNAPSHOT"
  :description "FIXME: write this!"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url  "http://www.eclipse.org/legal/epl-v10.html"}

  :min-lein-version "2.7.1"

  :dependencies [[org.clojure/clojure "1.9.0-alpha14"]
                 [org.clojure/clojurescript "1.9.229"]
                 [reagent "0.6.0"]
                 [re-frame "0.9.0"]]

  :plugins [[lein-figwheel "0.5.9"]
            [lein-cljsbuild "1.1.5" :exclusions [[org.clojure/clojure]]]]

  :source-paths ["assets/cljs"]

  :resource-paths ["assets"]

  :clean-targets ^{:protect false} ["assets/public/js/compiled"]

  :cljsbuild {:builds
              [{:id "dev"

                :source-paths ["assets/cljs"]

                ;; the presence of a :figwheel configuration here
                ;; will cause figwheel to inject the figwheel client
                ;; into your build
                :figwheel {:on-jsload "frontend.core/main"}

                :compiler {:main                 frontend.core
                           ;; Need to point to Figwheel dev server (localhost:3449),
                           ;; because assets are routed via Django in dev mode
                           :asset-path           "http://localhost:3449/js/compiled/out"
                           :output-to            "assets/public/js/compiled/frontend.js"
                           :output-dir           "assets/public/js/compiled/out"
                           :source-map-timestamp true

                           ;; To console.log CLJS data-structures make sure you enable devtools in Chrome
                           ;; https://github.com/binaryage/cljs-devtools
                           :preloads [devtools.preload]}}

               ;; This next build is an compressed minified build for
               ;; production. You can build this with:
               ;; lein cljsbuild once min
               {:id           "min"
                :source-paths ["assets/cljs"]
                :compiler     {:output-to     "assets/public/js/compiled/frontend.js"
                               :main          frontend.core
                               :optimizations :advanced
                               :pretty-print  false}}]}

  :figwheel {;; :server-port 3449 ;; default
             ;; :server-ip "127.0.0.1"

             :nrepl-port 7888

             ;; Watch and update CSS
             :css-dirs ["assets/public/css"]}


  :profiles {:dev {:dependencies [[binaryage/devtools "0.9.2"]
                                  [figwheel-sidecar "0.5.9"]
                                  [com.cemerick/piggieback "0.2.1"]]
                   :plugins      [[cider/cider-nrepl "0.15.0-SNAPSHOT"]]
                   :source-paths ["assets/cljs" "assets/dev"]
                   :repl-options {:nrepl-middleware [cemerick.piggieback/wrap-cljs-repl]}}})
