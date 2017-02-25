(defproject test "0.1.0-SNAPSHOT"
  :description "Empty"
  :cljsbuild {:builds
              {:dev {:compiler {:output-to "out/frontend2.js"}}
               :min {:compiler {:output-to "out/frontend2-min.js"}}}})
