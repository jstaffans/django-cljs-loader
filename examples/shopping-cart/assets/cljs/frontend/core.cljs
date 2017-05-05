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


(defn flatten-cart
  "Convert the cart into data suitable for a form POST.
  Django wants the form data organised in a particular way:

  {'items-0-cart': <cart id>,
   'items-0-id': <item id>,
   'items-0-name': <item name>,
   'items-0-quantity': <quantity>,
   ...}"
  [cart]
  (reduce-kv
   (fn [acc k item]
     (let [item-prefix (str "items-" k)]
       (assoc acc
              (str item-prefix "-cart") (get cart "id")
              (str item-prefix "-id") (get item "id")
              (str item-prefix "-name") (get item "name")
              (str item-prefix "-quantity") (get item "quantity"))))
   {}
   (into [] (get cart "items"))))

(defn with-management-form-data
  [flat-cart]
  (assoc
   flat-cart
   "items-TOTAL_FORMS" 3
   "items-INITIAL_FORMS" 3
   "items-MIN_NUM_FORMS" 1
   "items-MAX_NUM_FORMS" 1))

(defn as-form-data
  [flat-cart]
  (let [form-data (js/FormData.)
        _         (doseq [[k v] flat-cart]
                    (.set form-data k v))]
    form-data))

(rf/reg-event-fx
 :submit-cart
 (fn [cofx _]
   (let [form-data (-> cofx
                       :db
                       :cart
                       flatten-cart
                       with-management-form-data)]
     {:http-xhrio {:method          :post
                   :headers         {"X-CSRFToken" (cookies/get "csrftoken")}
                   :uri             "/"
                   :params          form-data
                   :format          (ajax.core/url-request-format)
                   :response-format (ajax.core/json-response-format {:keywords? true})
                   :on-success      [::post-ok]
                   :on-failure      [::post-error]}})))


;; TODO: success message
(rf/reg-event-db
 ::post-ok
 (fn [db _]
   (.log js/console "ok")
   db))

(rf/reg-event-db
 ::post-error
 (fn [db message]
   (.log js/console "error")
   (.log js/console message)
   db))

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
