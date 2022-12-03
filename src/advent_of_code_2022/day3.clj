(ns advent-of-code-2022.day3
  (:require [advent-of-code-2022.utils :as u]
            [clojure.set :as set]))

(defn split-evenly [x]
  (split-at (/ (count x) 2) x))

(defn priority [c]
  (if (u/between (int \a) (int \z) (int c))
    (+ 1 (- (int c) (int \a)))
    (+ 27 (- (int c) (int \A)))))

(defn shared-element [a b]
  (nth (take 1 (set/intersection (set a) (set b))) 0))

(defn line-priority [s]
  (let [[a b] (split-evenly s)]
    (priority (shared-element a b))))

(defn part1 [x]
  (let [lines (u/input-lines x)]
    (u/sum (map line-priority lines))))

(defn group-shared [g]
  (nth (take 1 (apply set/intersection (map set g))) 0))

(def group-priority (comp priority group-shared))

(defn part2 [x]
  (let [lines (u/input-lines x)]
    (u/sum (map group-priority (u/group-by-n 3 lines)))))