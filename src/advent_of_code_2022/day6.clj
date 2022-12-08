(ns advent-of-code-2022.day6
  (:require [advent-of-code-2022.utils :as u]
            [clojure.set :as set]
            [clojure.string :as str])
  (:import (clojure.lang PersistentQueue)))

(defn windows [coll n]
  (let [head (take n coll)
        tail (nthrest coll n)
        initial-queue (reduce conj PersistentQueue/EMPTY head)]
    (reverse
      (map seq
         (reduce (fn [a c]
              (cons
                (conj (pop (first a)) c)
                    a))
            (list initial-queue) tail)))))

(defn all-distinct? [coll]
  (= (count coll) (count (set coll))))

(defn part1 [x]
  (let [input (u/get-input x)
        wins (windows input 4)
        indexes (range 4 (count input))
        pairs (u/zip wins indexes)]
    (last (first (filter (comp all-distinct? first) pairs)))
    ))

(defn part2 [x]
  (let [input (u/get-input x)
        wins (windows input 14)
        indexes (range 14 (count input))
        pairs (u/zip wins indexes)]
    (last (first (filter (comp all-distinct? first) pairs)))
    ))