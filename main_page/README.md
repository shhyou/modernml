Format
=====
### Terms

- A JSON file containing array of terms, frequency from high to low

- Exapmle
    ```javascript
    "terms": ["DP", "Greedy", "DFS", "BFS"];
    ```

### ToC

- A JSON file containing ToC and array of book (or course), each item recording the link, title, topic

- Exapmle

    ```javascript
    [ { "toc": "Binary tree",
        "item": [{"title": "Introduction to Algorithms, third edition",
                  "href": "https://mitpress.mit.edu/books/introduction-algorithms",
                  "topic": "Binary search tree"},
                 {"title": "Algorithms (4th Edition)",
                  "href": "http://www.amazon.com/gp/product/032157351X/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=algs4-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=032157351X",
                  "topic": "R-B tree"},
                ...]
      }
      ...
    ]
    ```