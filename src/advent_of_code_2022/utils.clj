(ns advent-of-code-2022.utils)

(defn get-input [x]
  (let [filename (str "inputs/" x)]
    (slurp filename)))

(def lines clojure.string/split-lines)

(def input-lines (comp lines get-input))

(defn newline-separated-groups [x]
  (let [ls (lines x)
        groups (partition-by #(= "" %) ls)]
    (filter #(not= '("") %) groups)))

(def input-newline-separated-groups
  (comp newline-separated-groups get-input))

(defn sum [x]
  (reduce + x))
