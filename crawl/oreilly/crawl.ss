(use srfi-13) ; string library
(use srfi-11     :only (let-values))
(use rfc.http    :only (http-get http-post))
(use rfc.json    :only (parse-json construct-json))
(use sxml.sxpath :only (sxpath car-sxpath node-pos sxml:string-value))
(require "./htmlprag") ; html->sxml

(define *url/oreilly* "shop.oreilly.com")
(define *uri/category* "/category/browse-subjects.do")

(define *file/category* "category.json")

;; GET request to `shop.oreilly.com` (with proper delay)
;; string -> sxml
(define (get-oreilly uri)
  (let-values ([(response header content)
                (http-get *url/oreilly* uri)])
    (cond [(string=? response "200")
           (sys-sleep 31)                      ; sleep 31s
           (html->sxml content)]
          [(string=? response "404")
           response]
          [else
           (error (format #f "Getting url '~a' but got response '~a'"
                          uri response))])))

(define (update-index cats category)
  (let* ([url (assoc category cats)]
         [idx0 (get-oreilly url)])
    'TODO))

(define (update-category)
  ;; remove top-level categories such as
  ;;   "http://shop.oreilly.com/category/browse-subjects.do"
  ;;   "http://shop.oreilly.com/category/browse-subjects/programming.do"
  ;; by testing whether `s[:-3] + "/"` is the prefix of some other urls in the list
  (define (remove-top-lists xs)
    (filter
     (^s (not (member (string-append (string-drop-right s 3) "/") xs
                      (^[s1 s2] (or (string-prefix? s1 s2)
                                    (string-prefix? s2 s1))))))
     xs))
  
  (call-with-output-file *file/category*
    (lambda (port)
      (let* ([html (begin
                     (format #t "Retrieving HTML...\n")
                     (get-oreilly *uri/category*))]
             [urls (begin
                     (format #t "Extracting URLs...\n")
                     ($ remove-top-lists $
                        filter (^s (string-contains s "browse-subjects")) $
                        map sxml:string-value $
                        (sxpath '(// ul li a ^ href)) html))]
             [cats (map (^s (cons (substring
                                   s
                                   (string-length "http://shop.oreilly.com/category/browse-subjects/")
                                   (- (string-length s) 3))
                                  s))
                        urls)])
        (construct-json cats port)))))

(define (main args)
  (format #t "args: ~a\n" args)
  (update-category))
