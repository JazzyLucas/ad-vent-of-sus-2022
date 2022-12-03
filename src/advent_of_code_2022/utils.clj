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

(defn split-whitespace [s]
  (clojure.string/split s #"\s+"))

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