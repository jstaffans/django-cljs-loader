(defproject test "0.1.0-SNAPSHOT"
  :description ^{:some-key true} "Empty"
  ;; cljsbuild section
  :cljsbuild {:builds
              [{:id "dev"
                :compiler {:output-to "assets/public/out/frontend.js"}}
               {:id "min"
                :compiler {:output-to "assets/public/out/frontend-min.js"}}]})
