(use srfi-13) ; string library
(use srfi-11     :only (let-values))
(use rfc.http    :only (http-get http-post))
(use rfc.json    :only (parse-json construct-json))
(use sxml.sxpath :only (sxpath car-sxpath node-pos sxml:string-value))
(require "./htmlprag") ; html->sxml

(define *url/oreilly* "shop.oreilly.com")
(define *uri/category* "/category/browse-subjects.do")

(define *file/category* "category.json")


(define (update-category)
  ;; retrieve category list from oreilly
  (define (get-html)
    (let-values ([(response header content)
                  (http-get *url/oreilly* *uri/category*)])
      (when (not (equal? response "200"))
        (error (format #f "Getting url '~a' but got response '~a'" )))
      content))

  ;; select category hrefs (with some other urls)
  (define (select-categories html)
    ((sxpath '(// ul li a ^ href))(html->sxml html)))

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
                     (get-html))]
             [urls (begin
                     (format #t "Parsing URL...\n")
                     ($ remove-top-lists $
                        filter (^s (string-contains s "browse-subjects")) $
                        map sxml:string-value $
                        select-categories html))])
        (construct-json (list->vector urls) port)))))

(define (main args)
  (format #t "args: ~a\n" args)
  (update-category))
