(define (negative? num)
  (< num 0))

(define (positive? num)
  (> num 0))

(define (avg num_1 num_2)
  (/ (+ num_1 num_2) 2))

(define (decision? num_1 num_2)
  (< (abs (- num_1 num_2)) 0.0000001))

(define (half-interval func point_a point_b)

  (define (error name)
    (err name))

  (define (half-interval-method func point_a point_b)
    (let ((avg_point (avg point_a point_b)))
    (cond ((decision? point_a point_b)
           (avg point_a point_b))
           ((> (func avg_point) 0)
           (half-interval-method func point_a
                                      avg_point))
          ((< (func avg_point) 0)
           (half-interval-method func avg_point
                                      point_b)))))
  (cond ((and (negative? (func point_a))
              (positive? (func point_b)))
         (half-interval-method func point_a point_b))
        ((and (negative? (func point_b))
              (positive? (func point_a)))
         (half-interval-method func point_b point_a))
        (else (error "Числа одинаковых знаков!"))))

(define (increments num step)
    (+ num step))

(define (fixed-point func point)
  (let ((cur_point (func point)))
    (display point)
    (newline)
    (if (decision? cur_point point) cur_point
        (fixed-point func cur_point))))

(define (sqrt_ x)
  (fixed-point (lambda (y) (* (+ (/ x y) y) 0.5)) 1.0))

; 1.35

;(fixed-point (lambda (x) (+ 1 (/ 1 x))) 1.0)

; 1.36

;(fixed-point (lambda (x) (/ (log 1000) (log x))) 2.0)
;(fixed-point (lambda (x) (avg (/ (log 1000) (log x)) x)) 2.0)

; 1.37

; a)
(define (cont-frac n d k)
  (define (iter-cont-frac n d count result)
    (if (= count 0) result
        (iter-cont-frac n d (- count 1)
                            (/ (n count)
                               (+ (d count) result)))))
  (iter-cont-frac n d k 0.0))

; b)
(define (cont-fract n d k)
  (define (cont-frac-rec n d i)
    (if (= i k) (/ (n i) (d i))
        (/ (n i) (+ (d i)
                    (cont-frac-rec n d (+ i 1))))))
  (cont-frac-rec n d 1))

; 1.38

(define (d-eyler i)
  (if (= (remainder i 3) 2)
      (/ (* (+ i 1) 2) 3)
      1))

(define (exp k)
  (+ 2 (cont-fract (lambda (i) 1.0)
                    d-eyler
                    k)))

; 1.39

(define (tan-cf x k)
  (define (numerator i)
    (if (= i 1) x
        (* x x)))
  (define (tan-rec n d i)
    (if (< (- k 2) i) (/ (n i) (d i))
        (/ (n i) (- (d i)
                    (tan-rec n d (+ i 2))))))
  (tan-rec numerator (lambda (i) i) 1))

(define (avg-dump func)
  (lambda (x) (avg (func x) x)))

(define (sqrt__ x)
  (fixed-point (avg-dump (lambda (y) (/ x y))) 1.0))

(define (sqrt_3 x)
  (fixed-point (avg-dump (lambda (y) (/ x (* y y)))) 1.0))

(define (def-nc func)
        (lambda (point)
                (/ (- (func (+ point dx))
                (func point)) dx)))

(define dx 0.00001)

(define (method-newton func guess)
        (define (newton-fun g)
          (- g (/ (func g)
               ((def-nc func) g))))
        (fixed-point newton-fun guess))

(define (coub x)
  (* x x x))

; 1.40

(define (cubic a b c)
  (lambda (x) (+ (* x x x)
                 (* a x x)
                 (* b x)
                 c)))

; 1.41

(define (double func)
  (lambda (x)
    (func (func x))))

(define (inc x)
  (+ x 1))

; 1.42

(define (compose fun_f fun_g)
  (lambda (x)
    (fun_f (fun_g x))))

; 1.43

(define (repeated func num)
  (define (repeated-iter func count result)
    (if (= count 1)
        result
        (repeated-iter func (- count 1)
                            (func result))))
  (lambda (x) (repeated-iter func num (func x))))

; 1.44

(define (smoothed func)
  (lambda (x)
    (/ (+ (func (- x dx))
          (func x)
          (func (+ x dx))) 3)))

(define (smoothed-repeated func num)
  (lambda (x)
          (((repeated smoothed num) func) x)))

; 1.45

