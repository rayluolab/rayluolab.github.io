---
title: Contribute a note
summary: How lab members can write and submit a note.
type: page
---

Notes are short explanations, paper discussions, and practical guides written
by lab members. Each note shows its contributors and date. New notes appear at
the top of the [Notes page](/post/).

## 1. Start a note

[Start a note on GitHub →](https://github.com/rayluolab/rayluolab.github.io/new/main?filename=content%2Fpost%2Fyour-note-title%2Findex.md&value=---%0Atitle%3A+Your+note+title%0Asummary%3A+One+or+two+sentences+explaining+what+readers+will+learn.%0Aauthors%3A%0A++-+Your+Name%0Adate%3A+2026-10-15T09%3A00%3A00-07%3A00%0Adraft%3A+true%0Anote_type%3A+Explainer%0Atags%3A+%5B%5D%0A---%0A%0A%23%23+The+question%0A%0AIntroduce+the+question+and+who+the+note+is+for.%0A%0A%23%23+Explanation%0A%0AExplain+the+idea+in+your+own+words.%0A%0A%23%23+References%0A%0ALink+the+sources+you+used.%0A)

Change `your-note-title` to a unique folder name and fill in the template.

Add a Markdown file to the
[website repository](https://github.com/rayluolab/rayluolab.github.io/tree/main/content/post).
Give each note its own folder, for example
`content/post/2026-10-15-your-topic/index.md`. Images can go in the same folder.

Use this header, replacing the title, summary, author, and date:

```yaml
---
title: Your note title
summary: One or two sentences explaining what readers will learn.
authors:
  - Your Name
date: 2026-10-15T09:00:00-07:00
draft: true
note_type: Explainer
tags:
  - Your topic
---
```

Use your name exactly as it appears on the [People page](/people/), such as
`Jocelyn Lin` or `Ivan Perez`. For a joint contribution, add each contributor
on a separate line under `authors`.

The `note_type` can be `Explainer`, `Reading note`, or `Practical guide`.

## 2. Write and submit

Write below the header using Markdown. Explain one question clearly, include
references, and credit any reused figures. Submit a pull request to the
repository's `main` branch. Repository write access is not required to propose
a change through a fork and pull request.

Keep `draft: true` while the note is being reviewed. Drafts are excluded from
the deployed website. For local draft previews, run `hugo server --buildDrafts`.

## 3. Publish after review

When the note is ready, set `draft: false` and merge the approved change into
`main`. The existing website deployment then publishes it. The Notes list sorts
by the note's `date`, newest first. Updating a note does not change its original
publication date; use `lastmod` for a later revision date.

If your name is missing from People, include a request to add your author
profile with the submission.
