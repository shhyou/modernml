(use srfi-13) ; string library
(use srfi-11     :only (let-values))
(use scheme.time :only (current-second))
(use rfc.http    :only (http-get http-post))
(use rfc.json    :only (parse-json construct-json))
(use sxml.sxpath :only (sxpath car-sxpath node-pos sxml:string-value sxml:child-nodes))
(require "./htmlprag") ; html->sxml

; delay between GET requests (in seconds)
(define *get-delay* 10)

(define *url/oreilly* "shop.oreilly.com")
(define *uri/category* "/category/browse-subjects.do")

(define *file/category* "category")
(define *file/list* '"list-")

;; GET request to `shop.oreilly.com` (with proper delay)
;; string -> sxml
(define get-oreilly
  (let ([t 0])
    (lambda (uri)
      (let [(t^ (- (current-second) t))]
        (when (<= t^ *get-delay*)
          (sys-sleep (inexact->exact (ceiling (- (+ *get-delay* 1) t^))))))
      (let-values ([(response header content)
                    (http-get *url/oreilly* uri)])
        (set! t (current-second))
        (cond [(string=? response "200")
               (html->sxml content)]
              [(member response '("400" "401" "403" "404"))
               response]
              [else
               (error (format #f "Getting url '~a' but got response '~a'"
                              uri response))])))))

; category list -> category -> ()
(define (update-index cats cat)
  (define select-pages
      (let ([query (sxpath '(// ((select) (^ name (equal? "dirPage"))) option ^ value))])
        (lambda (html)
          (let* ([option-values (map sxml:string-value (query html))]
                 [hrefhref (filter (^s (string-contains s "browse-subjects")) option-values)])
            (take hrefhref (/ (length hrefhref) 2))))))
    (define (get-pages idx0)
      (let ([hrefs (select-pages idx0)])
        (cond [(null? hrefs)
               (list idx0)]
              [else (display "Retrieving pages") (flush)
                    (let ([pages
                           (map (lambda (href)
                                  (display ".") (flush)
                                  (get-oreilly href))
                                hrefs)])
                      (format #t "\n")
                      pages)])))
    (define select-books
      (sxpath '(// table tr ((td) (^ class (equal? "thumbtext"))) div div a)))
    (define (extract-book-info book)
      `((title . ,(car ((node-pos 2) (sxml:child-nodes book))))
        (local_href . ,(sxml:string-value ((car-sxpath '(^ href)) book)))))
    (let* ([url (cdr (assoc "href" (cdr (assoc cat cats))))]
           [idx0 (begin
                   (format #t "Retrieving the first page...\n")
                   (get-oreilly url))]
           [pages (get-pages idx0)]
           [books (begin
                    (format #t "Extracting books...\n")
                    (apply append (map select-books pages)))]
           [booksinfo (map extract-book-info books)])
      (call-with-output-file (string-append (cdr (assoc "file" (cdr (assoc cat cats)))))
        (lambda (port)
          (let ([json (list->vector booksinfo)])
            (construct-json (list->vector booksinfo) port)
            json)))))

; () -> ()
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

  (call-with-output-file (string-append *file/category* ".json")
    (lambda (port)
      (define get-category
        (let ([prefix-len (string-length "http://shop.oreilly.com/category/browse-subjects/")])
          (lambda (url)
            (substring url prefix-len (- (string-length url) 3)))))
      (let* ([html (begin
                     (format #t "Retrieving HTML...\n")
                     (get-oreilly *uri/category*))]
             [urls (begin
                     (format #t "Extracting URLs...\n")
                     ($ remove-top-lists $
                        filter (^s (string-contains s "browse-subjects")) $
                        map sxml:string-value $
                        (sxpath '(// ul li a ^ href)) html))]
             [cats (map (^s (let ([cat (get-category s)])
                              `(,cat
                                . ((href . ,s)
                                   (file . ,(string-append
                                             *file/list*
                                             (string-join (string-split cat "/") ",")
                                             ".json"))))))
                        urls)])
        (construct-json cats port)
        cats))))

'(
  "example usage"

  (define cats         ;; create category list
    (update-category))
  (define cats         ;; use this if category list already exists
    (call-with-input-file (string-append *file/category* ".json") read))

  ;; create book list for category 'programming/csharp'
  (update-index cats "programming/csharp")
  )
