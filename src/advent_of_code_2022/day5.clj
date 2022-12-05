(ns advent-of-code-2022.day5
  (:require [advent-of-code-2022.utils :as u]
            [clojure.set :as set]
            [clojure.string :as str]))

(defn parse-crate-line [x]
  (let [parts (u/group-by-n 4 x)]
    (map #(nth % 1) parts)))

(defn parse-command [x]
  (let [parts (u/split-whitespace x)
        [amt src dst] (map read-string (list (nth parts 1) (nth parts 3) (nth parts 5)))]
        (list amt (- src 1) (- dst 1))))


(defn make-stacks [crate-lines]
  (defn pad-to-len [len line]
    (concat line (map (constantly \space) (range len))))
  (let [amt (reduce max (map count crate-lines))
        padded-lines (map #(pad-to-len amt %) crate-lines)
        crate-maps (map u/seq-to-index-map padded-lines)
        ]
    (defn make-stack-i [i]
      (drop-while #(= \space %) (map #(get % i) crate-maps)))
    (u/seq-to-index-map (map make-stack-i (range amt)))))

(defn exec-command [stacks cmd]
  (defn pop-n [n i]
    (list (take n (get stacks i)) (nthrest (get stacks i) n)))
  (defn push-n [elems i]
    (reduce (fn [a c] (cons c a)) (get stacks i) elems))
  (let [[amount src dst] cmd
        [popped rest] (pop-n amount src)
        pushed (push-n popped dst)]
    (assoc (assoc stacks src rest) dst pushed)))

(defn parse-stacks [ls]
  (let [actual-ls (reverse (nthrest (reverse ls) 1))]
    (map parse-crate-line actual-ls)))

(defn parse-commands [ls]
  (map parse-command ls))

(defn parse-input [x]
  (let [[crates commands] (u/input-newline-separated-groups x)]
    (list (make-stacks (parse-stacks crates)) (parse-commands commands))))

(defn part1 [x]
  (let [[stacks commands] (parse-input x)
        updated-stacks (u/index-map-to-seq (reduce exec-command stacks commands))]
    (apply str (map #(nth % 0) updated-stacks))))


(defn exec-command2 [stacks cmd]
  (defn pop-n [n i]
    (list (take n (get stacks i)) (nthrest (get stacks i) n)))
  (defn push-n [elems i]
    (reduce (fn [a c] (cons c a)) (get stacks i) (reverse elems)))
  (let [[amount src dst] cmd
        [popped rest] (pop-n amount src)
        pushed (push-n popped dst)]
    (assoc (assoc stacks src rest) dst pushed)))

(defn part2 [x]
  (let [[stacks commands] (parse-input x)
        updated-stacks (u/index-map-to-seq (reduce exec-command2 stacks commands))]
    (apply str (map #(nth % 0) updated-stacks))))
