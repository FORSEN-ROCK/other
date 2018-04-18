;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_1_3) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (pow x)
  (* x x)
)

(define (my_abs x)
  (cond ((>= x 0)
        x)
        ((< x 0)
        (- x))))

(define (max_n num_1 num_2)
        (if (> num_1 num_2)
            num_1
            num_2))

(define (sqrt_max_sum a b c)
  (if (> a b)
       (+ (pow (max a b)) (pow (max_n b c)))
       (+ (pow (max a b)) (pow (max_n a c)))))

(define (avg x y)
        (/ (+ x y) 2))

(define (improve guess var)
  (avg guess (/ var guess)))

(define (good-guess? var guess)
  (<= (my_abs (- (pow guess) var)) 0.001))

(define (sqrt-item guess var)
  (if (good-guess? var guess)
       guess
       (sqrt-item (improve guess var)
                  var)))

(define (my_sqrt var)
  (sqrt-item 1.0 var))

(define (good-guess_new? guess_old guess_new)
  (< (my_abs (- guess_old guess_new)) (* 10e-8 guess_new)))

(define (sqrt-item_new guess guess_old var)
  (if (good-guess_new? guess_old guess)
       guess
       (sqrt-item_new (improve guess var)
                  guess
                  var)))

(define (my_sqrt_new var)
  (sqrt-item_new 1.0 0.0 var))


