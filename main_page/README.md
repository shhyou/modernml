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
    "toc" : [ { "topic": "Dynamic Programming",
                "item": [{"title": "Introduction to Algorithms, third edition",
                          "href": "http://example.com",
                          "topic": "DP"},
                         {"title": "Algorithms (4th Edition)",
                          "href": "http://example.com",
                          "topic": "Dynamic Programming"},
                         {"title": "Data structure and Algorithms",
                          "href": "http://example.com",
                          "topic": "動態規劃"},
                        ...]
              },
              { "topic": "binary search tree",
                "item": [{"title": "Introduction to Algorithms, third edition",
                          "href": "http://example.com",
                          "topic": "binary search tree"},
                         {"title": "Algorithms (4th Edition)",
                          "href": "http://example.com",
                          "topic": "binary tree"},
                        ...]
              },
              ...
            ]
    ```