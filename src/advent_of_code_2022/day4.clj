(ns advent-of-code-2022.day4
  (:require [advent-of-code-2022.utils :as u]
            [clojure.set :as set]
            [clojure.string :as str]))

(defn parse-assignment [s]
  (map read-string (str/split s #"-")))

(defn assignment_contains [a b]
  (let [[al, ar] a
        [bl, br] b]
    (and (<= al bl) (<= al br) (>= ar bl) (>= ar br))))

(defn either-contains [a b]
  (or (assignment_contains a b) (assignment_contains b a)))

(defn parse-line [x]
  (let [ranges (str/split x #",")]
    (map parse-assignment ranges)))

(defn assignment-overlaps [a b]
  (let [[al, ar] a
        [bl, br] b]
    (or (and (>= ar bl) (<= al br)) (and (>= br al) (<= bl ar)))))
(defn part1 [x]
  (let [lines (u/input-lines x)
        parsed-lines (map parse-line lines)]
    (count (filter #(apply either-contains %) parsed-lines))))

(defn part2 [x]
  (let [lines (u/input-lines x)
        parsed-lines (map parse-line lines)]
    (count (filter #(apply assignment-overlaps %) parsed-lines))))
