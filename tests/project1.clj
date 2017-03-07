(defproject test "0.1.0-SNAPSHOT"
  :description ^{:some-key true} "Empty"

  ;; cljsbuild section
  :cljsbuild {:builds
              [{:id "dev"
                :compiler {:output-to "assets/public/out/frontend.js"}
                :figwheel {:on-jsload "frontend.core/run"}}
               {:id "min"
                :compiler {:main frontend.core
                           :output-to "assets/public/out/frontend-min.js"}}]})
