(ns advent-of-code-2022.core
  (:require [advent-of-code-2022.utils :as utils]
            [advent-of-code-2022.day3 :as day3]
            [advent-of-code-2022.day4 :as day4]))

(defn day1 [x]
  (let [groups (utils/input-newline-separated-groups x)
        ints (map #(map read-string %) groups)
        sums (map utils/sum ints)]
    (reduce max sums)))

(defn day1-b [x]
  (let [groups (utils/input-newline-separated-groups x)
        ints (map #(map read-string %) groups)
        sums (map utils/sum ints)]
    (take 3 (reverse (sort sums)))))

(defn day2 [x]
  (defn score [a b]
    (let [shape-score (case b
                        "X" 1
                        "Y" 2
                        "Z" 3)
          round-score (case (list a b)
                        (("A" "X")) 3
                        (("A" "Y")) 6
                        (("A" "Z")) 0
                        (("B" "X")) 0
                        (("B" "Y")) 3
                        (("B" "Z")) 6
                        (("C" "X")) 6
                        (("C" "Y")) 0
                        (("C" "Z")) 3)]
      (+ shape-score round-score)))
  (let [line-pairs (utils/input-line-fields x)
        scores (map #(apply score %) line-pairs)]
    (utils/sum scores)))

(defn day2-b [x]
  (defn score [a b]
    (let [outcome-score (case b
                          "X" 0
                          "Y" 3
                          "Z" 6)
          shape-score (case (list a b)
                        (("A" "X")) 3
                        (("B" "X")) 1
                        (("C" "X")) 2
                        (("A" "Y")) 1
                        (("B" "Y")) 2
                        (("C" "Y")) 3
                        (("A" "Z")) 2
                        (("B" "Z")) 3
                        (("C" "Z")) 1)]
      (+ shape-score outcome-score)))
  (let [line-pairs (utils/input-line-fields x)
        scores (map #(apply score %) line-pairs)]
    (utils/sum scores)))
