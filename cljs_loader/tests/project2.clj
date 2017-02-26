(defproject test "0.1.0-SNAPSHOT"
  :description "Empty"
  :figwheel {:server-port 3000}
  :cljsbuild {:builds
              {:dev {:compiler {:output-to "out/frontend2.js"}}
               :min {:compiler {:output-to "out/frontend2-min.js"}}}})
