# mdBuilder

![PyPI - Version](https://img.shields.io/pypi/v/mdBuilder)

## NOTICE

This library is just a **TOY PROJECT**!

DON'T use it in production environment!

## Installation

```python
pip install mdBuilder
```

## Usage

### Basic Syntax

#### Headings

Markdown:

```markdown
# Heading level 1
## Heading level 2
### Heading level 3  
#### Heading level 4  
##### Heading level 5  
###### Heading level 6
```

Python:

```Python
Heading(1, "Heading level 1")
Heading(2, "Heading level 2")
Heading(3, "Heading level 3")
Heading(4, "Heading level 4")
Heading(5, "Heading level 5")
Heading(6, "Heading level 6")
```

#### Paragraphs

Markdown:

```markdown
I really like using Markdown.

I think I'll use it to format all of my documents from now on. 
```

Python:

```Python
Paragraph("I really like using Markdown.")
Paragraph("I think I'll use it to format all of my documents from now on.")
```

#### Emphasis

##### Bold

Markdown:

```markdown
I just love **bold text**.
Love**is**bold
```

Python:

```Python
Paragraph("I just love ", Bold("bold text"), ".")
Paragraph("Love", Bold("is"), "bold")
```

##### Italic

Markdown:

```markdown
Italicized text is the *cat's meow*.
A*cat*meow
```

Python:

```Python
Paragraph("Italicized text is the ", Italic("cat's meow"), ".")
Paragraph("A", Italic("cat"), "meow")
```

##### Bold and Italic

Markdown:

```markdown
This text is ***really important***.
This is really***very***important text.
```

Python:

```Python
Paragraph("This text is ", BoldItalic("really important"), ".")
Paragraph("This is really", BoldItalic("very"), "important text.")
```

#### Blockquotes

Markdown:

```markdown
> Dorothy followed her through many of the beautiful rooms in her castle.
```

Python:

```Python
Blockquote("Dorothy followed her through many of the beautiful rooms in her castle.")
```

##### Blockquotes with Multiple Paragraphs

Markdown:

```markdown
> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
```

Python:

```Python
Blockquote(
    "Dorothy followed her through many of the beautiful rooms in her castle.", 
    "The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.")
```

##### Nested Blockquotes

Markdown:

```markdown
> Dorothy followed her through many of the beautiful rooms in her castle.
>
>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.
```

Python:

```Python
Blockquote(
    "Dorothy followed her through many of the beautiful rooms in her castle.", 
    Blockquote("The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood."))
```

##### Blockquotes with Other Elements

Markdown:

```markdown
> #### The quarterly results look great!
>
> * Revenue was off the chart.
> * Profits were higher than ever.
>
>  *Everything* is going according to **plan**.
```

Python:

```Python
Blockquote(
    Heading(4, "The quarterly results look great!"),
    UnorderedList(
        "Revenue was off the chart.",
        "Profits were higher than ever."
    ),
    Paragraph(Italic("Everything"), " is going according to ", Bold("plan"), ".")
)
```

#### Lists

##### Ordered Lists

Markdown:

```markdown
1. First item
2. Second item
3. Third item
4. Fourth item 

1. First item
2. Second item
3. Third item
    1. Indented item
    2. Indented item
4. Fourth item 
```

Python:

```Python
OrderedList(
    "First item",
    "Second item",
    "Third item",
    "Fourth item"
)

OrderedList(
    "First item",
    "Second item",
    ["Third item",
    OrderedList(
        "Indented item",
        "Indented item")],
    "Fourth item"
)
```

##### Unordered Lists

Markdown:

```markdown
* First item
* Second item
* Third item
* Fourth item 

* First item
* Second item
* Third item
    * Indented item
    * Indented item
* Fourth item 
```

Python:

```Python
UnorderedList(
    "First item",
    "Second item",
    "Third item",
    "Fourth item"
)

UnorderedList(
    "First item",
    "Second item",
    ["Third item",
    UnorderedList(
        "Indented item",
        "Indented item")],
    "Fourth item"
)
```

##### Adding Elements in Lists

###### Paragraphs

Markdown:

```markdown
* This is the first list item.
* Here's the second list item.

    I need to add another paragraph below the second list item.

* And here's the third list item.
```

Python:

```Python
UnorderedList(
    "This is the first list item.",
    ["Here's the second list item.",
    Paragraph("I need to add another paragraph below the second list item.")],
    "And here's the third list item."
)
```

###### Blockquotes

Markdown:

```markdown
* This is the first list item.
* Here's the second list item.

    > A blockquote would look great below the second list item.

* And here's the third list item.
```

Python:

```Python
UnorderedList(
    "This is the first list item.",
    ["Here's the second list item.",
    Blockquote("A blockquote would look great below the second list item.")],
    "And here's the third list item."
)
```

###### Images

Markdown:

```markdown
1. Open the file containing the Linux mascot.
2. Marvel at its beauty.

    ![Tux, the Linux mascot](/assets/images/tux.png)

3. Close the file.
```

Python:

```Python
OrderedList(
    "Open the file containing the Linux mascot.",
    ["Marvel at its beauty.",
    Image(path_or_url="/assets/images/tux.png", alt_text="Tux, the Linux mascot")],
    "Close the file."
)
```

###### Lists

Markdown:

```markdown
1. First item
2. Second item
3. Third item
    * Indented item
    * Indented item
4. Fourth item
```

Python:

```Python
OrderedList(
    "First item",
    "Second item",
    ["Third item",
    UnorderedList(
        "Indented item",
        "Indented item"
    )],
    "Fourth item"
)
```

#### Code

Markdown:

```markdown
At the command prompt, type `nano`.
```

Python:

```Python
Paragraph("At the command prompt, type ", Code("nano"), ".")
```

#### Horizontal Rules

Markdown:

```markdown
---
```

Python:

```Python
HorizontalRule()
```

#### Links

Markdown:

```markdown
My favorite search engine is [Duck Duck Go](https://duckduckgo.com).
```

Python:

```Python
Paragraph("My favorite search engine is ",
          Link(url="https://duckduckgo.com", text_or_image="Duck Duck Go"),
          ".")
```

##### Adding Titles

Markdown:

```markdown
My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").
```

Python:

```Python
Paragraph("My favorite search engine is ",
          Link(url="https://duckduckgo.com", 
               text_or_image="Duck Duck Go", 
               title="The best search engine for privacy"),
          ".")
```

##### URLs and Email Addresses

Markdown:

```markdown
<https://www.markdownguide.org>
<fake@example.com>
```

Python:

```Python
Link(url="https://www.markdownguide.org")
Link(url="fake@example.com")
```

##### Formatting Links

Markdown:

```markdown
I love supporting the [**EFF**](https://eff.org).
This is the [*Markdown Guide*](https://www.markdownguide.org).
See the section on [`code`](#code).
```

Python:

```Python
Paragraph("I love supporting the ", 
          Link(url="https://eff.org", text_or_image=Bold("EFF")), 
          ".")
Paragraph("This is the ", 
          Link(url="https://www.markdownguide.org", text_or_image=Italic("Markdown Guide")), 
          ".")
Paragraph("See the section on ", 
          Link(url="#code", text_or_image="code"), 
          ".")
```

#### Images

Markdown:

```markdown
![The San Juan Mountains are beautiful!](/assets/images/san-juan-mountains.jpg "San Juan Mountains")

```

Python:

```Python
Image(path_or_url="/assets/images/san-juan-mountains.jpg", alt_text="The San Juan Mountains are beautiful!", title="San Juan Mountains")
```

##### Linking Images

Markdown:

```markdown
[![An old rock in the desert](/assets/images/shiprock.jpg "Shiprock, New Mexico by Beau Rogers")](https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv)


```

Python:

```Python
Link(
    url="https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv", 
    text_or_image=Image(
        path_or_url="/assets/images/shiprock.jpg", 
        alt_text="ImAn old rock in the desertage", 
        title="Shiprock, New Mexico by Beau Rogers")
)
```

### Extened Syntax

#### Tables

Markdown:

```markdown
| Syntax | Description |
| --- | --- |
| Header | Title |
| Paragraph | Text |
```

Python:

```Python
Table(
    headers=["Syntax", "Description"],
    content=[
        ["Header", "Title"],
        ["Paragraph". "Text"]
    ]
)
```

##### Alignment

Markdown:

```markdown
| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |
```

Python:

```Python
Table(
    header=["Syntax", "Description", "Test Text"],
    content=[
        ["Header", "Title", "Here's this"],
        ["Paragraph". "Text", "And more"]
    ],
    alignment=[
        Alignment.LEFT,
        Alignment.CENTER,
        Alignment.RIGHT
    ]
)
```

#### Fenced Code Blocks

Markdown:

`````markdown
```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
`````

Python:

```Python
FencedCodeBlock(
    "{\n"+
    "  \"firstName\": \"John\"\n"+
    "  \"lastName\": \"Smith\"\n"+
    "  \"age\": 25\n"+
    "}"
)
```

##### Syntax Highlighting

Markdown:

`````markdown
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
`````

Python:

```Python
FencedCodeBlock(
    "{\n"+
    "  \"firstName\": \"John\"\n"+
    "  \"lastName\": \"Smith\"\n"+
    "  \"age\": 25\n"+
    "}",
    syntax="json"
)
```

#### Strikethrough

Markdown:

```markdown
~~The world is flat.~~ We now know that the world is round.
```

Python:

```Python
Paragraph(
    Strikethrough("The world is flat."),
     " We now know that the world is round.")
```

#### Task Lists

Markdown:

```markdown
- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
```

Python:

```Python
TaskList(
    ("Write the press release", "x"),
    "Update the website",
    "Contact the media"
)
```

## TODO

- [ ] HTML
- [ ] Heading IDs
- [ ] Definition Lists
- [ ] Highlight
- [ ] Subscript
- [ ] Superscript

## Reference

The markdown string format refers to <https://www.markdownguide.org/>

## LICENSE

This project is published under [MIT License](https://github.com/mill413/mdBuilder/blob/main/LICENSE).
