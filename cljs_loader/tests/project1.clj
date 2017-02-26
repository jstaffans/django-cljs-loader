(defproject test "0.1.0-SNAPSHOT"
  :description ^{:some-key true} "Empty"
  ;; cljsbuild section
  :cljsbuild {:builds
              [{:id "dev"
                :compiler {:output-to "out/frontend.js"}}
               {:id "min"
                :compiler {:output-to "out/frontend-min.js"}}]})
