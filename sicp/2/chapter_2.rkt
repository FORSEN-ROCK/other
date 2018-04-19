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