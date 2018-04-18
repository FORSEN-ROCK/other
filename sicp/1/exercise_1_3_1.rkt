(define (sum term a next b)
  (if (> a b)
      0
      (+ (term a)
         (sum term (next a) next b))))

(define (int num)
  (+ num 1))

(define (sum-int a b)
  (sum + a int b))

(define (coub a)
  (* a a a))

(define (sum-coub a b)
  (sum coub a int b))

(define (sum-pi a b)
  (define (item-pi a)
    (/ 1.0  (* a (+ a 2))))
  (define (next-item a)
    (+ a 4))
  (sum item-pi a next-item b))

(define (integral function a b defirencial)
  (define (add-dx a)
    (+ a defirencial))
  (* (sum function (+ a (/ defirencial 2)) add-dx b) defirencial))

;exercise 1.29

(define (my_even? num)
  (= (remainder (/ num 2) 2) 0))

(define (simpson function a b n)
  (define (argument a b counter)
    (+ a (/ (* (- b a) counter) n)))
  (define (decor-fun num)
    (cond ((or (= num 0)
                (= num n))
            (function (argument a b num)))
           ((= (remainder num 2) 0)
            (* (function (argument a b num)) 2))
           (else (* (function (argument a b num)) 4))))
  (* (/ (- b a) (* n 3))
     (sum decor-fun 0 int n)))

(define (iter-remainder num remainder_num)
  (cond ((> (- remainder_num num) 0)
            (iter-remainder num (- remainder_num num)))
        (else remainder_num)))

(define (% num_1 num_2)
  (iter-remainder num_2 num_1))

; 1.30
(define (sum-iter term a next b)
  (define (sum-iter a result)
    (if (> a b)
        result
        (sum-iter (next a) (+ result (term a)))))
  (sum-iter a 0))

(define (sum-int-iter a b)
  (sum-iter + a int b))

; 1.31
;a)
(define (product term a next b)
  (if (> a b)
      1
      (* (term a)
         (product term (next a) next b))))

(define (! num)
  (product * 1 int num))

(define (approx-pi b)
  (define (pi-item num)
    (* (/ (* num 2) (- (* num 2) 1))
       (/ (* num 2) (+ (* num 2) 1))))
  (* 0.5 (product pi-item 1 int b))) 

;b)
(define (product-iter term a next b)
  (define (prod-iter a result)
    (if (> a b)
        result
        (prod-iter (next a) (* result (term a)))))
    (prod-iter a 1))

(define (factorial-iter num)
  (product-iter * 1 int num))

; 1.32
;a)
(define (accomulate combiner null-value term a next b)
  (if (> a b)
      null-value
      (combiner (term a)
                 (accomulate combiner null-value term (next a) next b))))

(define (accum-rec-sum term a next b)
  (define (cond-sum var_1 var_2)
    (+ var_1 var_2))
  (accomulate cond-sum 0 term a next b))

(define (accum-rec-prod term a next b)
  (define (cond-mult var_1 var_2)
    (* var_1 var_2))
  (accomulate cond-mult 1 term a next b))

;b)
(define (accomulate-iter combiner null-value term a next b)
  (define (accum-iter num result)
    (if (> num b)
        result
        (accum-iter (next num)
                    (combiner result (term num)))))
    (accum-iter a null-value))

(define (accum-iter-sum term a next b)
  (define (cond-sum var_1 var_2)
    (+ var_1 var_2))
  (accomulate-iter cond-sum 0 term a next b))

(define (accum-iter-prod term a next b)
  (define (cond-mult var_1 var_2)
    (* var_1 var_2))
  (accomulate-iter cond-mult 1 term a next b))

; 1.33
(define (filtered-accumulate combiner filter null-value term a next b)
  (define (filter-accum-iter num result)
    (cond ((> num b) result)
          ((filter num)
           (filter-accum-iter (next num)
                              (combiner result (term num))))
          (else (filter-accum-iter (next num)
                                   result))))
  (filter-accum-iter a null-value))

(define (filter-accum-rec combiner filter null-value term a next b)
  (cond ((> a b) null-value)
        ((filter a)
         (combiner (term a)
                   (filter-accum-rec combiner filter null-value
                                     term (next a) next b)))
        (else (combiner (filter-accum-rec combiner filter
                              null-value term (next a) next b)
                        (filter-accum-rec combiner filter
                              null-value term (next (next a)) next b)))))
                                                  
                                     
(define (coub-sum-even a b)
  (define (even? num)
    (= (remainder num 2) 0))
  
  (define (cond-sum var_1 var_2)
    (+ var_1 var_2))

  (filtered-accumulate cond-sum even? 0 coub a int b))