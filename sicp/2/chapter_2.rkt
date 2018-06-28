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
;(define A (make-point 0 10))
;(define B (make-point 10 10))
;(define D (make-point 0 2))
;(define rec-ABCD (make-rectangle A B D))
;(define P (rec-perimetr rec-ABCD))
;(define S (rec-area rec-ABCD))
;(define A1 (make-point (- 1) 6))
;(define B1 (make-point 5 5))
;(define D1 (make-point (- 2) (- 2)))
;(define rec-A1B1D1 (make-rectangle A1 B1 D1))
;(define P1 (rec-perimetr rec-A1B1D1))
;(define S1 (rec-area rec-A1B1D1))

; 2.4

(define (cons_ x y)
(lambda (m) (m x y)))

(define (car_ z)
(z (lambda (p q) p)))

(define (cdr_ z)
  (z (lambda(p q) q)))

; (car_ (cons_ 1 2))
; (car (lambda (m) (m 1 2)))
; ((lambda (m) (m 1 2)) (lambda (p q) p))
; ((lambda ( p q) p) 1 2)
; 1

; 2.5

(define (pow base n)
  (define (square num)
      (* num num))
  (define (even? num)
      (= (remainder num 2) 0))
  (define (pow-iter base n prod)
      (cond ((= n 0) prod)
            ((even? n) (pow-iter (square base) (/ n 2) prod))
            (else (pow-iter base (- n 1) (* prod base)))))
  (pow-iter base n 1))
        

(define (cons_n a b)
  (* (pow 2 a)
     (pow 3 b)))

(define (car_n num)
  (define (car-iter z)
    (if (= (remainder z 3) 0)
        (car-iter (/ z 3))
        z))
  (/ (log (car-iter num))
     (log 2)))

(define (cdr_n num)
  (define (cdr-iter z)
    (if (= (remainder z 2) 0)
        (cdr-iter (/ z 2))
        z))
  (/ (log (cdr-iter num))
     (log 3)))

; 2.6 Не решена

(define zero (lambda (f) (lambda (x) x)))

(define (add-1 n)
  (lambda (f) (lambda (x) (f ((n f) x)))))

; 2.7
(define (add-interval int_1 int_2)
  (make-interval (+ (lower-interval int_1)
                    (lower-interval int_2))
                 (+ (upper-interval int_1)
                    (upper-interval int_2))))

(define (mult-interval int_1 int_2)
  (let ((p_1 (* (lower-interval int_1)
                (lower-interval int_2)))
        (p_2 (* (upper-interval int_1)
                (upper-interval int_2)))
        (p_3 (* (lower-interval int_1)
                (upper-interval int_2)))
        (p_4 (* (upper-interval int_1)
                (upper-interval int_2))))
    (make-interval (min p_1 p_2 p_3 p_4)
                   (max p_1 p_2 p_3 p_4))))

(define (div-interval int_1 int_2)
  (mult-interval int_1
                 (make-interval (/ 1.0 (upper-interval int_2))
                                (/ 1.0 (lower-interval int_2)))))

(define (lower-interval int)
  (car int))

(define (upper-interval int)
  (cdr int))

(define (make-interval min_int max_int)
  (cons min_int max_int))

; test
(define r1 (make-interval 6.12 7.48))
(define r2 (make-interval 4.47 4.94))
(define ro1 (add-interval r1 r2))
(define ro2 (mult-interval r1 r2))
(define ro3 (div-interval r1 r2))

; 2.8
(define (sub-interval int_1 int_2)
  (add-interval int_1
                (make-interval (- (lower-interval int_2))
                               (- (upper-interval int_2)))))
; test
(define sub-int (sub-interval (make-interval 2 3)
                              (make-interval 4 5)))

; 2.9 написать доказательство
; 2.10
(define (new-dev-interval int_1 int_2)
  (if (and (< (lower-interval int_2) 0)
           (> (upper-interval int_2) 0))
      "Error denum is zero!"
      (div-interval int_1 int_2)))

; 2.11 астично решена
(define (make-center-wigth center wigth)
  (make-interval (- center wigth)
                 (+ center wigth)))

(define (center int)
  (/ (+ (upper-interval int)
        (lower-interval int)) 2))

(define (wigth int)
  (/ (- (upper-interval int)
        (lower-interval int)) 2))

; 2.12
(define (make-center-percent center error)
  (make-interval (* center (- 1 (/ error 100)))
                 (* center (+ 1 (/ error 100)))))
(define (percent int)
  (* (/ (wigth int)
        (center int)) 100))

; 2.13
; Погрешность произведения приблизительно равна
; сумме погрешностей исходных интервалов
; !! Написать вывод

; 2.14
(define (part_1 r1 r2)
  (let ((one (make-interval 1 1)))
    (div-interval one
                  (add-interval 
                      (div-interval one r1)
                      (div-interval one r2)))))

(define (part_2 r1 r2)
  (div-interval (mult-interval r1 r2)
                (add-interval r1 r2)))
; Утверждение, что алгебраически эквивалентные вырожения
; Дают различные результаты верно. Это вызвано суммированием
; погрешностей исходных итервалов при умножении, в следствии чего
; увилечение числа вычислительных операций приводет к увиличению
; погрешности. По этому алгебраически эквивалентные формы вычесления
; дают различные результаты при разном количестве вычилительных операций

; 2.15
; Да, права. Так как погрешность "концентрируется" в неточных велечинах
; многократные повторения и различные операции увеличивают погрешность
; результата. Пусть A и B - некотрые переменные величены с соответствующими
; погрешностями Ea и Eb. Тогда используя преблизительную формулу для опре-
; деления погрешности результата можно записать погрешности для обоих вариантов
; вычисления сопративления:
; 1) Ea * Eb
; 2) (Ea + Eb) / (Ea * Eb)
; По представленным формулам хорошо видно, для первого случая погрешность
; стремиться к 0  для всех интервалов с погрешностью меньше 100%.
; В втором случаее погрешность стримиться к бесконечности

; 2.16
; Первая часть описана в ответах на другие вопросы данного раздела.
; Для реализации пакета интервальной арифметики, не подверженного
; проблеме расхождения результатов необходимо реализовать так чтобы
; операции не влияли на погрешность результата. Возможно имеет смысл 
; для расчета использовать значения центров интервалов и последующем 
; вычислением результирующей погрешности

(define (my-length-iter items)
  (define (length-iter items count)
    (if (null? items)
        count
        (length-iter (cdr items) (+ count 1))))
  (length-iter items 0))

(define (my-length-rec items)
  (define (length-rec items)
    (if (null? items)
        0
        (+ 1 (length (cdr items)))))
  (length-rec items))

(define (get-n items n)
  (define (get-iter items count n)
    (if (= count n)
        (car items)
        (get-iter (cdr items) (+ 1 count) n)))
  (get-iter items 0 n))

(define (append item_1 item_2)
  (if (null? item_1)
      item_2
      (cons (car item_1)
            (append (cdr item_1) item_2))))

; 2.17
(define (last-pair-1 items)
  (list (get-n items (- (length items) 1))))

(define (last-pair-2 items)
  (define (iter items)
    (if (null? (cdr items))
        (list (car items))
        (iter (cdr items))))
  (iter items))

; 2.18
(define (reverse items)
  (define (reverse-rec items count)
    (if (= count 0)
        (cons (car items) null)
        (cons (get-n items count)
              (reverse-rec items (- count 1)))))
  (reverse-rec items (- (length items) 1)))

; 2.19
; 2.20
(define (same-parity num . nums)
  (define (even? num)
    (= (remainder num 2) 0))
  
  (define (noeven? num)
    (not (even? num)))
  
  (define (tensor-seq tensor nums)
    (cond ((null? nums) null)
          ((tensor (car nums))
           (cons (car nums)
              (tensor-seq tensor (cdr nums))))
          (else (tensor-seq tensor (cdr nums)))))
  
 (if (even? num)
     (tensor-seq even? nums)
     (tensor-seq noeven? nums)))

(define (map tensor sequence)
  (define (ierator nums)
    (if (null? nums) null
        (cons (tensor (car nums))
              (ierator (cdr nums)))))
  (ierator sequence))

; 2.21
(define (square-list nums)
  (if (null? nums) null
      (cons (* (car nums) (car nums))
            (square-list (cdr nums)))))

(define (square-lst nums)
  (map (lambda (x) (* x x)) nums))

; 2.22
; 1) Обратный порядок вызван тем что значение answer инициализировано 
;    null для первого шага, из-за чего получается "раскрутка списка с
;    конца"
; 2) Программа не работает так как структура списка предполагает, следующию 
;    сигнатуру: (list 1 2 3) == (cons 1 (cons 2 (cons 3 null))).
;    в рассматриваемом примере получается (cons (cons (cons null 1) 4) 9)

; 2.23
(define (my-for-each tensr nums)
  (if (null? nums) null
      (tensr (car nums)))
  (if (not (null? (cdr nums)))
      (my-for-each tensr (cdr nums))))

(define (count-leaves tree)
  (cond ((null? tree) 0)
        ((not (pair? tree)) 1)
        (else (+ (count-leaves (car tree))
                 (count-leaves (cdr tree))))))
  
; 2.25
; (car (cdr (car (cdr (cdr x)))))
; (car (car y))
; (car (cdr (car (cdr (car (cdr (car (cdr (car (cdr (car (cdr z))))))))))))

; 2.26
; ( 1 2 3 (4 5 6))      -- ( 1 2 3 4 5 6)
; ((1 2 3) . (4 5 6))   -- ((1 2 3) 4 5 6)
; ((1 2 3) (4 5 6))     ++

; 2.27
(define (deep-reverse sequence)
  (define (iter nums result)
          (cond ((null? nums) result)
                ((not (pair? (car nums))) (iter (cdr nums)
                                          (cons (car nums)
                                                 result)))
                (else (iter (cdr nums)
                            (cons (iter (car nums) null)
                                  result)))))
  (iter sequence null))

; 2.28
;(define (fringe sequence)
;  (define (iter nums result)
;    (cond ((null? nums) result)
;          ((not (pair? (car nums))) (iter (cdr nums)
;                                          (cons (car nums)
;                                                result)))
;          (else (iter (cdr nums) (cons (car (car nums))
;                                       result)))))
;  (iter sequence null))

(define (fringe items)
  (define (rec nums)
    (cond ((null? nums) null)
          ((not (pair? (car nums)))
           (cons (car nums)
                 (rec (cdr nums))))
          (else (append (cons (car (car nums))
                            (rec (cdr (car nums))))
                      (rec (cdr nums))))))
  (rec items))

; 2.29 Не делал

; Нужно подправить append что бы можно было обрабатывать листья
(define (map-tree tensor tree)
  (define (rec tree)
    (cond ((null? tree) null)
          ((pair? (car tree)) (append (list (map tensor (car tree)))
                                     (rec (cdr tree))))))
  (rec tree))

; 2.30
(define (square-tree-m tree)
  (map-tree (lambda (x) (* x x)) tree))

(define (square-tree tree)
  (define (square x)
    (* x x))
  (define (rec tree)
    (cond ((null? tree) null)
          ((not (pair? tree)) (square tree))
          (else (cons (rec (car tree))
                      (rec (cdr tree))))))
  (rec tree))

; 2.31 решена в рамках самостоятельного творчества
; 2.32 Не решена
(define (subset s)
  (define (logic x) s)
  (if (null? s) (list null)
      (let ((rest (subset (cdr s))))
           (append rest
                   (map logic rest)))))

; Раздел 2.2.3
(define (filter-my predicat sequence)
  (cond ((null? sequence) null)
        ((not (pair? sequence))
              (if (predicat sequence)
                  sequence))
        (else (if (predicat (car sequence))
                  (cons (filter predicat (car sequence))
                        (filter predicat (cdr sequence)))
                  (filter predicat (cdr sequence))))))

(define (filter predicat sequence)
  (cond ((null? sequence) null)
        ((predicat (car sequence))
         (cons (car sequence)
               (filter predicat (cdr sequence))))
        (else (filter predicat (cdr sequence)))))
             
(define (accumulate-my operation inicial sequence)
  (if (null? sequence)
      inicial
      (accumulate operation (operation (car sequence) inicial)
                  (cdr sequence))))

(define (accumulate operation inicial sequence)
  (if (null? sequence) inicial
      (operation (car sequence)
          (accumulate operation inicial (cdr sequence)))))

(define (enum-interval low higth)
  (if (> low higth) null
      (cons low (enum-interval (+ low 1) higth))))

(define (enum-tree tree)
  (cond ((null? tree) null)
        ((pair? (car tree)) (add (car tree)
                                 (cdr tree)))
        (else (cons (car tree)
                    (enum-tree (cdr tree))))))
      
(define (add sequence  sequence_2)
  (if (null? sequence) sequence_2
      (cons (car sequence)
            (add (cdr sequence) sequence_2))))

(define (square x)
  (* x x))

(define (odd? x)
  (not (= (remainder x 2) 0)))

(define (sum-odd-tree tree)
  (accumulate + 0
              (map square
                   (filter odd?
                           (enum-tree tree)))))
                           