;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_1_8) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (pow x)
  (* x x)
)

(define (avg x y)
        (/ (+ x y) 2))

(define (my_abs x)
  (cond ((>= x 0)
        x)
        ((< x 0)
        (- x))))

(define (qoup_improve x y)
        (/ (+ (/ x (pow y))
                   (* 2 y)) 3))

(define (improve guess var)
  (avg guess (qoup_improve var guess)))

(define (good-guess_new? guess_old guess_new)
  (< (my_abs (- guess_old guess_new)) (* 10e-4 guess_new)))

(define (sqrt-item_new guess guess_old var)
  (if (good-guess_new? guess_old guess)
       guess
       (sqrt-item_new (improve guess var)
                  guess
                  var)))

(define (my_sqrt_qoup var)
  (sqrt-item_new 1.0 0.0 var))