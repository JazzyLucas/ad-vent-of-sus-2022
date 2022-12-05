(ns advent-of-code-2022.utils
  (:require [clojure.set :as set]
            [clojure.string :as str]))

(defn get-input [x]
  (let [filename (str "inputs/" x)]
    (slurp filename)))

(def lines str/split-lines)

(def input-lines (comp lines get-input))

(defn newline-separated-groups [x]
  (let [ls (lines x)
        groups (partition-by #(= "" %) ls)]
    (filter #(not= '("") %) groups)))

(def input-newline-separated-groups
  (comp newline-separated-groups get-input))

(defn sum [x]
  (reduce + x))

(defn split-whitespace [s]
  (str/split s #"\s+"))

(def line-fields (comp #(map split-whitespace %) lines))

(def input-line-fields (comp line-fields get-input))

(defn between [a b x]
  (if (> a b)
    (between b a x)
    (and (>= x a) (<= x b))))

(defn group-by-n [n x]
  (defn go [i output input]
    (if (empty? input)
      output
      (let [[head & tail] input]
        (if (= i 0)
          (go 1 (cons (list head) output) tail)
          (let
            [[ohead & otail] output]
            (go
              (mod (+ i 1) n)
              (cons (cons head ohead) otail)
              tail)))))
    )
  (reverse (map reverse (go 0 '() x))))

(defn seq-to-index-map [seq]
  (defn reducer [a c]
    (let [[current-map, idx] a]
      (list (conj current-map [idx, c]) (+ idx 1))))
  (nth (reduce reducer [{} 0] seq) 0))

(defn index-map-to-seq [index-map]
  (defn go [idx result]
    (if (contains? index-map idx)
      (go (+ idx 1) (cons (get index-map idx) result))
      result))
  (reverse (go 0 '())))