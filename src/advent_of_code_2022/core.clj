(ns advent-of-code-2022.core
  (:require [advent-of-code-2022.utils :as utils]))

(defn day1 [x]
  (let [groups (utils/input-newline-separated-groups x)
        ints (map #(map read-string %) groups)
        sums (map utils/sum ints)]
    (reduce max sums)))
