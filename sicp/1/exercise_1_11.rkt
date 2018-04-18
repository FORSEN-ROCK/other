;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_1_11) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (f-recur num)
  (if (< num 3)
      num
      (+ (f-recur (- num 1))
         (f-recur (- num 2))
         (f-recur (- num 3)))))



(define (f-iter num_1 num_2 num_3 count)
  (if (= count 0)
      num_3
      (f-iter (+ num_1 num_2 num_3)
              num_1
              num_2
              (- count 1))))

(define (iter num)
  (f-iter 2 1 0 num))