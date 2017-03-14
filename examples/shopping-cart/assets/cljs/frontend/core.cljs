(ns frontend.core
  (:require [reagent.core :as reagent]
            [re-frame.core :as rf]))


(rf/reg-event-db
  :initialize
  (fn [db [_ initial-cart]]
    {:cart initial-cart}))


(rf/reg-sub
  :cart
  (fn [db _]
    (-> db
        :cart)))

(defn cart
  []
  [:div
   [:pre
    (str @(rf/subscribe [:cart]))]])

(defn ui
  []
  [:div
   [:h3 "Hello from ClojureScript/re-frame!"]
   [cart]])

;; -- Entry Point -------------------------------------------------------------

(defn ^:export main
  []
  (rf/dispatch-sync [:initialize (.-initialProps js/window)])
  (reagent/render [ui] (js/document.getElementById "app")))
