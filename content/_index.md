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

        The Ray Luo Lab at UC Irvine develops computational methods — molecular
        dynamics, polarizable force fields, and implicit-solvent models — to
        understand biomolecular structure and function at atomic detail. The
        group is led by Prof. Ray Luo (Molecular Biology & Biochemistry;
        Biomedical Engineering; Chemical Engineering & Materials Science).
      cta:
        label: Explore our research
        url: research/
      cta_alt:
        label: Publications
        url: publication/
    design:
      background:
        color: '#ffffff'

  - block: markdown
    content:
      title:
      text: |
        ![Luo Lab](/uploads/luo-lab-logo.png)
    design:
      columns: '1'
      css_class: home-brand

  - block: markdown
    content:
      title: Research Interests
      text: |
        At the heart of our work are biomolecules. Through the lens of
        computational physics, chemistry, and biology, we develop reliable,
        efficient methods to predict the structures, functions, and
        interactions of complex molecular systems — and to interpret the
        information encoded in genomes from physical and chemical principles.
    design:
      columns: '1'

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
