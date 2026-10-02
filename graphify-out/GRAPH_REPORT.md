# Graph Report - FloodLens-AI  (2026-10-03)

## Corpus Check
- 6 files · ~6,980 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 111 nodes · 105 edges · 7 communities (4 shown, 3 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `51802731`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]

## God Nodes (most connected - your core abstractions)
1. `Definition of Done` - 22 edges
2. `code:md (# FloodLens AI — Agent Workflow)` - 1 edges
3. `code:block2` - 1 edges
4. `code:block3` - 1 edges
5. `code:block4` - 1 edges
6. `code:block5` - 1 edges
7. `code:block6` - 1 edges
8. `code:block7` - 1 edges
9. `code:block8` - 1 edges
10. `code:block9` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (7 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (43): code:md (# FloodLens AI — Project State), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+35 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (23): code:md (# FloodLens AI — Agent Workflow), code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16 (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (22): code:block10, code:block11, code:block12, code:block13, code:block14, code:block15, code:block16, code:block17 (+14 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (14): code:md (# FloodLens AI — System Prompt), code:block2, code:block3, code:block4, code:block5, code:block6, Dependencies, Files to Create (+6 more)

## Knowledge Gaps
- **104 isolated node(s):** `code:md (# FloodLens AI — Agent Workflow)`, `code:block2`, `code:block3`, `code:block4`, `code:block5` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Definition of Done` connect `Community 2` to `Community 3`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **What connects `code:md (# FloodLens AI — Agent Workflow)`, `code:block2`, `code:block3` to the rest of the system?**
  _104 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.045454545454545456 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._