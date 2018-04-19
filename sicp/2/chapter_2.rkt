(define (gcd num_1 num_2)
  (if (= num_2 0) num_1
      (gcd num_2 (remainder num_1 num_2))))

(define (make-rat n d)
  (cons n d))

(define (numer num)
  (car num))

(define (denom num)
  (cdr num))

(define (add-rat num_1 num_2)
  (make-rat (+ (* (numer num_1)
                  (denom num_2))
               (* (numer num_2)
                  (denom num_1)))
            (* (denom num_1)
               (denom num_2))))

(define (sub-rat num_1 num_2)
  (make-rat (- (* (numer num_1)
                  (denom num_2))
               (* (numer num_2)
                  (denom num_1)))
            (* (denom num_1)
               (denom num_2))))

(define (mult-rat num_1 num_2)
  (make-rat (* (numer num_1)
               (numer num_2))
            (* (denom num_1)
               (denom num_2))))

(define (div-rat num_1 num_2)
  (make-rat (* (numer num_1)
               (denom num_2))
            (* (numer num_2)
               (denom num_1))))

(define (equal-rat? num_1 num_2)
  (= (* (numer num_1)
        (denom num_2))
     (* (numer num_2)
        (denom num_1))))

(define (print-rat num)
  (display (numer num))
  (display "/")
  (display (denom num))
  (newline))

(define (make-rat-opt n d)
  (let ((num-gcd (gcd n d)))
        (make-rat (/ n num-gcd)
                  (/ d num-gcd))))

; 2.1
; Assuming: (- a) = (make-rat (- numer) (-denom))

(define (sign-rat n d)
  (if (or (< n 0)
          (< d 0))
      (- 1)
      1))

(define (maker-rat n d)
  (let ((num-gcd (gcd n d))
        (sign (sign-rat n d)))
    (cons (* sign (/ n num-gcd))
          (abs (/ d num-gcd)))))

(define (mult-rat-opt num_1 num_2)
    (maker-rat (* (numer num_1)
                  (numer num_2))
               (* (denom num_1)
                  (denom num_2))))

; test
;(define a (maker-rat (- 3) (- 5)))
;(define b (maker-rat 2 7))
;(define c (maker-rat (- 3) 8))
;(define d (maker-rat 1 (- 3)))
;(define e (mult-rat-opt a b))
;(define f (maker-rat 4 (- 16)))