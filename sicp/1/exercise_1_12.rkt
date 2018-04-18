;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname exercise_1_12) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(define (pascal-recurs row_num elm_num)
  (cond ((= row_num 1) 1)
        ((and (> row_num 0)
              (> elm_num 0)
              (<= elm_num row_num))
         (+ (pascal-recurs (- row_num 1)
                           (- elm_num 1))
            (pascal-recurs (- row_num 1)
                           (+ elm_num 1))))
        (else 0)))