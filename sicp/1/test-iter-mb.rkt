;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname test-iter-mb) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (square num)
  (* num num))

(define (my_even? num)
  (= (remainder num 2) 0))

(define (expmod_mb num_n pow num_m)
  (cond ((= pow 1) num_n)
        ((my_even? pow)
          (remainder-chech? (expmod_mb num_n (/ pow 2) num_m) num_m))
        (else (remainder (* num_n (expmod_mb num_n (- pow 1) num_m))
                         num_m))))

(define (remainder-chech? exp_num num)
  (root_1? exp_num num (remainder (square exp_num) num)))


(define (root_1? num_n num_m exp_num)
  (if (and (not (= num_n 1))
           (not (= num_n (- num_m 1)))
           (= exp_num 1))
      0
      exp_num))

(define (root? num)
  (if (= num 1)
      0
      num))

(define (not-prime? num counter)
  (> counter (/ num 2)))
                                  
(define (try-ai-bm num rand_num)
    (= (expmod_mb rand_num (- num 1) num) rand_num))

(define (test-miller-rabin num)
  (try-ai-bm num (random (- num 1))))

(define (test-iter-mb num repid count)
  (cond ((and (= repid 0)
              (not (not-prime? num count))) true)
        ((test-miller-rabin num)
         (test-iter-mb num (- repid 1) count))
        ((not (test-miller-rabin num))
         (test-iter-mb num (- repid 1) (+ count 1)))
        (else false)))