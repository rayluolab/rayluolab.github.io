---
# Leave the homepage title empty to use the site title
title:
date: 2026-06-05
type: landing

sections:
  - block: hero
    content:
      title:
      image:
        filename: people/portrait-small.png
      text: |
        ### Welcome to the Ray Luo Lab

        **Ray Luo**, Principal Investigator

        - Professor, Molecular Biology &amp; Biochemistry — School of Biological Sciences
        - Professor, Biomedical Engineering — Henry Samueli School of Engineering
        - Professor, Chemical Engineering &amp; Materials Science — Henry Samueli School of Engineering

        **Education**

        - B.S., Beijing University, 1990 — Biophysics
        - Ph.D., University of Maryland at College Park, 1998 — Chemistry

        **Research interests:** Computational analysis of biomolecular sequence, structure, dynamics, and function.
      cta:
        label: Explore our research
        url: research/
      cta_alt:
        label: Publications
        url: publication/

  - block: markdown
    content:
      title:
      text: |
        ![Luo Lab](/uploads/luo-lab-logo-transparent.png)

        At the heart of our work are biomolecules. Through the lens of
        computational physics, chemistry, and biology, we develop reliable,
        efficient methods to predict the structures, functions, and
        interactions of complex molecular systems — and to interpret the
        information encoded in genomes from physical and chemical principles.
    design:
      columns: '1'
      css_class: home-brand

  - block: collection
    content:
      title: Research Areas
      text: ''
      filters:
        folders:
          - research
    design:
      view: card
      columns: '2'

  - block: collection
    content:
      title: Recent Publications
      text: ''
      count: 5
      filters:
        folders:
          - publication
        publication_type: ''
      order: desc
    design:
      view: citation
      columns: '1'
---
