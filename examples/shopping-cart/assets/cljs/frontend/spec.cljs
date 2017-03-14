(ns frontend.spec
  (:require [clojure.spec :as s]))

(s/def :item/name string?)
(s/def :item/quantity int?)

(s/def :cart/item (s/keys :req [:item/name :item/quantity]))

(s/def :cart/items (s/coll-of :cart/item))

(s/def ::cart (s/keys :req [::items]))

