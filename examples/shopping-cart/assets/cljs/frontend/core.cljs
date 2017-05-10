(ns frontend.core
  (:require [reagent.core :as reagent]
            [reagent.cookies :as cookies]
            [re-frame.core :as rf]
            [day8.re-frame.http-fx]
            [cognitect.transit :as t]))

;; This is a hypothetical frontend for a shopping cart. The initial cart
;; data is read from a JSON string put into a script tag by the server.
;; After updates have been performed, the new cart can be POSTed back
;; via a normal form POST.


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
  "Add metadata that Django needs to parse the form data correctly.
  TODO: would be a lot better to do a JSON POST and not mimic the way
  server-side rendered Django forms work."
  [flat-cart]
  (let [num-items (/ (count flat-cart) 4)]  ;; each item produces four form parameters
    (assoc
     flat-cart
     "items-TOTAL_FORMS" num-items
     "items-INITIAL_FORMS" num-items
     "items-MIN_NUM_FORMS" num-items
     "items-MAX_NUM_FORMS" num-items)))

(defn as-form-data
  "Create a FormData object with the flattened cart, ready to be POSTed to Django."
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


(rf/reg-event-db
 ::post-ok
 (fn [db _]
   (assoc db :message {:text "Successfully updated cart!" :type :success})))

(rf/reg-event-db
 ::post-error
 (fn [db message]
   (.log js/console "error")
   (.log js/console message)
   (assoc db :message {:text "An error occurred." :type :error})))

(rf/reg-sub
 :cart
 (fn [db _]
   (:cart db)))


(rf/reg-sub
 :items
 :<- [:cart]
 (fn [cart _]
   (get cart "items")))


(rf/reg-sub
 :message
 (fn [db _]
   (:message db)))


;; -----------------------------------------------------------------------------
;; UI
;; -----------------------------------------------------------------------------


(defn inc-item
  [qty]
  (min (inc qty) 10))


(defn dec-item
  [qty]
  (max (dec qty) 0))


(defn item
  [{name "name", quantity "quantity"} line-item]
  [:li {:key name}
   [:span (str name, ", " quantity)]
   [:span
    [:a {:href "#" :on-click #(rf/dispatch [:update-item-quantity name inc-item])} "+"]
    [:a {:href "#" :on-click #(rf/dispatch [:update-item-quantity name dec-item])} "-"]]])


(defn cart
  []
  [:div
   [:ul.cart
    (map item @(rf/subscribe [:items]))]])


(defn message
  []
  (let [msg @(rf/subscribe [:message])]
    (when msg
      [:h4.message (:text msg)])))

(defn on-submit
  [e]
  (.preventDefault e)
  (rf/dispatch [:submit-cart]))


(defn ui
  []
  [:form {:method "POST" :on-submit on-submit}
   [:div
    [:h3 "Please update your fruity order here:"]
    [cart]
    [:input {:type "submit"}]
    [message]]])


;; -----------------------------------------------------------------------------
;; Entry point
;; -----------------------------------------------------------------------------

(def reader (t/reader :json))

(defn ^:export main
  []
  (rf/dispatch-sync [:initialize (t/read reader (.-initialProps js/window))])
  (reagent/render [ui] (js/document.getElementById "app")))
