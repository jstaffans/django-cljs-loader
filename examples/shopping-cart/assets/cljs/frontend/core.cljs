(ns frontend.core
  (:require [reagent.core :as reagent]
            [reagent.cookies :as cookies]
            [re-frame.core :as rf]
            [day8.re-frame.http-fx]
            [cognitect.transit :as t]))


;; -----------------------------------------------------------------------------
;; Events, subscriptions
;; -----------------------------------------------------------------------------

(rf/reg-event-db
  :initialize
  (fn [db [_ initial-cart]]
    {:cart initial-cart}))


(defn update-quantity-fn
  "Updates the quantity of an item using the provided function if predicate matches."
  [pred f]
  (fn [item]
    (if (pred item)
      (update item "quantity" f)
      item)))


(defn name-matches-pred
  [name]
  #(= name (get % "name")))


(rf/reg-event-db
 :update-item-quantity
 (fn [db [_ item-name f]]
   (update-in db [:cart "items"] (partial map (update-quantity-fn (name-matches-pred item-name) f)))))


(defn cart-as-form-data
  [cart]
  )

(rf/reg-event-fx
 :submit-cart
 (fn [cofx _]
   (let [data (doto (js/FormData.)
                (.set "foo" "bar"))]
     {:http-xhrio {:method          :post
                   :headers         {"X-CSRFToken" (cookies/get "csrftoken")}
                   :uri             "/"
                   :data            data
                   :format          (ajax.core/text-request-format)
                   :response-format (ajax.core/json-response-format {:keywords? true})
                   :on-success      [::good-post-result]
                   :on-failure      [::bad-post-result]}})))


(rf/reg-sub
  :cart
  (fn [db _]
    (:cart db)))


(rf/reg-sub
 :items
 :<- [:cart]
 (fn [cart _]
   (get cart "items")))


;; -----------------------------------------------------------------------------
;; UI
;; -----------------------------------------------------------------------------

(defn item
  [{name "name", quantity "quantity"} line-item]
  [:li {:key name}
   [:span (str name, ", " quantity)]
   [:span
    [:span.action {:on-click #(rf/dispatch [:update-item-quantity name inc])} "+"]
    [:span.action {:on-click #(rf/dispatch [:update-item-quantity name dec])} "-"]]])


(defn cart
  []
  [:div
   [:ul.cart
    (map item @(rf/subscribe [:items]))]])


(defn on-submit
  [e]
  (.preventDefault e)
  (rf/dispatch [:submit-cart]))


(defn ui
  []
  [:form {:method "POST" :on-submit on-submit}
   [:div
    [:h3 "Please update your fruity order here!"]
    [cart]
    [:input {:type "submit"}]]])


;; -----------------------------------------------------------------------------
;; Entry point
;; -----------------------------------------------------------------------------

(def reader (t/reader :json))

(defn ^:export main
  []
  (rf/dispatch-sync [:initialize (t/read reader (.-initialProps js/window))])
  (reagent/render [ui] (js/document.getElementById "app")))
