;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_1_2_6) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (smallest-divisor n)
  (find-divisor n 2))

(define (square num)
  (* num num))

(define (find-divisor n test-count)
  (cond ((num-divisor? n test-count) n)
        ((divisor? n test-count) test-count)
        (else (find-divisor n (+ test-count 1)))))

(define (num-divisor? num_1 num_2)
  (> (square num_2) num_1))

(define (divisor? num_1 num_2)
  (= (remainder num_1 num_2) 0))

(define (prime? num)
  (= (smallest-divisor num) num))

(define (my_even? num)
  (= (remainder num 2) 0))

(define (expmod num_n pow num_m)
  (cond ((= pow 0) 1)
        ((my_even? pow)
          (remainder (square (expmod num_n (/ pow 2) num_m))
                    num_m))
        (else (remainder (* num_n (expmod num_n (- pow 1) num_m))
                         num_m))))

(define (try-ai num rand_num)
    (= (expmod rand_num num num) rand_num))

(define (test-ferma num)
  (try-ai num (random (- num 1))))

(define (test-iter num repid)
  (cond ((= repid 0) true)
        ((test-ferma num)
         (test-iter num (- repid 1)))
        (else false)))

(define (next test-divisor)
  (if (= test-divisor 2) 3
      (+ test-divisor 2)))

(define (find-divisor-opt n test-count)
  (cond ((num-divisor? n test-count) n)
        ((divisor? n test-count) test-count)
        (else (find-divisor n (next test-count)))))

(define (smallest-divisor-opt n)
  (find-divisor-opt n 2))

