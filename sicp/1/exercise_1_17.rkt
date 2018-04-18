;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_1_17) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (multiplication a b)
  (if (= b 0) 0
      (+ a (multiplication a (- b 1)))))

(define (double num)
  (+ num num))

(define (halve num)
  (/ num 2))

(define (multi-iter num_1 num_2 product)
  (cond ((= num_2 0) product)
        (else (multi-iter num_1
                          (- num_2 1)
                          (+ product num_1)))))

(define (multi num_1 num_2)
  (multi-iter num_1 num_2 0))

(define (my_even? n)
(= (remainder n 2) 0))

;1.17
(define (multi-expt num_1 num_2)
  (cond ((= num_2 0) 0)
        ((my_even? num_2) (multi-expt (double num_1)
                                      (halve num_2)))
        (else (+ num_1 (multi-expt
                                  num_1
                                  (- num_2 1))))))


;1.18
(define (multi-expt-iter num_1 num_2 invariant)
  (cond ((= num_2 0) invariant)
        ((my_even? num_2) (multi-expt-iter (double num_1)
                                            (halve num_2)
                                            invariant))
        (else (multi-expt-iter num_1
                               (- num_2 1)
                               (+ invariant num_1)))))

(define (multiplication-expt num_1 num_2)
  (multi-expt-iter num_1 num_2 0))