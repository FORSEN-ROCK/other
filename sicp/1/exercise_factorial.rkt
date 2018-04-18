;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_factorial) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (factorial num)
  (if (= num 1)
      1
      (* num (factorial (- num 1)))))

(define (fact num)
  (define (equal-num? num counter)
    (= num counter))
  
  (define (fact-iter num counter)
    (if (equal-num? num counter)
        num
        (* counter (fact-iter num (+ counter 1)))))
  
  (fact-iter num 1))
