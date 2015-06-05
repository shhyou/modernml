Crawler Data
=====
### Where to put data
- Put it in `linuxXX.csie.org:/tmp2/YY/(apress|mit|oreilly)`

    * FIXME: choose `XX` and `YY`

### Storing Format

- A JSON file containing array of books, each item recording *at least* the link, title, category and table of contents of a book

- Both category and ToC are lists of strings. For table of contents, title of sections are treated as title of chapters

- Exapmle

    ```javascript
    [ { "href": "http://shop.oreilly.com/product/0636920032519.do",
        "title": "Fluent Python",
        "category: ["programming", "python"],
        "toc": ["The Python Data Model",
                "An Array of Sequences",
                "Dictionaries and Sets",
                ...] },
      { "href": "http://shop.oreilly.com/product/0636920023784.do",
        "title": "Python for Data Analysis",
        "category": ["programming", "python"],
        "toc": ["Preliminaries",                 // chapter 1
                "What Is This Book About?",      // section 1.1
                "Why Python for Data Analysis?", // section 1.2
                ...,
                "Introductory Examples",         // chapter 2
                "1.usa.gov data from bit.ly",    // section 2.1
                "MovieLens 1M Data Set",         // section 2.2
                ...] },
      ...
    ]
    ```
