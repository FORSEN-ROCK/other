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

; 2.2

(define (make-point x y)
  (cons x y))

(define (point-x point)
  (car point))

(define (point-y point)
  (cdr point))

(define (print-point point)
  (display "(")
  (display (point-x point))
  (display " , ")
  (display (point-y point))
  (display ")")
  (newline))

(define (make-segment begin_p end_p)
  (cons begin_p end_p))

(define (start-segment segment)
  (car segment))

(define (end-segment segment)
  (cdr segment))

(define (mid-point-segment segment)
  (make-point (/ (+ (point-x (start-segment segment))
                    (point-x (end-segment segment))) 2)
              (/ (+ (point-y (start-segment segment))
                    (point-y (end-segment segment))) 2)))

; test
;(define point-a (make-point 2 4))
;(define point-b (make-point 8 6))
;(define segment-a (make-segment point-a point-b))
;(define mid-point-ab (mid-point-segment segment-a))
;(define point-c (make-point (- 2) (- 3)))
;(define point-d (make-point 4 (- 1)))
;(define segment-b (make-segment point-c point-d))
;(define mid-point-cd (mid-point-segment segment-b))

; 2.3

; a
;(define (make-rectangle ver-a ver-b ver-d)
;  (cons (make-segment ver-a ver-d)
;        (make-segment ver-a ver-b)))

;(define (len-segment segment)
;  (let ((projection-x (- (point-x (end-segment segment))
;                         (point-x (start-segment segment))))
;        (projection-y (- (point-y (end-segment segment))
;                         (point-y (start-segment segment)))))
;    (sqrt (+ (* projection-x projection-x)
;             (* projection-y projection-y)))))

;(define (rec-height rectangel)
;  (len-segment (car rectangel)))

;(define (rec-width rectangel)
;  (len-segment (cdr rectangel)))

; b

(define (make-rectangle ver-a ver-b ver-d)
  (let ((height-x (- (point-x ver-d)
                     (point-x ver-a)))
        (height-y (- (point-y ver-d)
                     (point-y ver-a)))
        (width-x (- (point-x ver-b)
                    (point-x ver-a)))
        (width-y (- (point-y ver-b)
                    (point-y ver-a))))
  (cons (sqrt (+ (* height-x height-x)
                 (* height-y height-y)))
        (sqrt (+ (* width-x width-x)
                 (* width-y width-y))))))

(define (rec-height rectangel)
  (car rectangel))

(define (rec-width rectangel)
  (cdr rectangel))

(define (rec-area rectangel)
  (let ((height (rec-height rectangel))
         (width (rec-width rectangel)))
    (* height width)))

(define (rec-perimetr rectangel)
  (let ((height (rec-height rectangel))
        (width (rec-width rectangel)))
    (+ (* 2 height)
       (* 2 width))))

;test
(define A (make-point 0 10))
(define B (make-point 10 10))
(define D (make-point 0 2))
(define rec-ABCD (make-rectangle A B D))
(define P (rec-perimetr rec-ABCD))
(define S (rec-area rec-ABCD))
(define A1 (make-point (- 1) 6))
(define B1 (make-point 5 5))
(define D1 (make-point (- 2) (- 2)))
(define rec-A1B1D1 (make-rectangle A1 B1 D1))
(define P1 (rec-perimetr rec-A1B1D1))
(define S1 (rec-area rec-A1B1D1))