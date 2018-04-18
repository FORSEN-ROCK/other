;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_1_16) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (my_even? n)
   (= (remainder n 2) 0))

(define (pow num p invariant)
  (cond ((= p 0) invariant)
        ((my_even? p) (pow (square num)
                           (/ p 2)
                           invariant))
        (else (pow num
              (- p 1)
              (* num invariant)))))

(define (fast-pow num p)
  (pow num p 1))

(define (square num)
  (* num num))

(define (fast-expt b n)
  (cond ((= n 0) 1)
        ((even? n) (fast-expt (square b) (/ n 2)))
        (else (* b (fast-expt b (- n 1))))))
