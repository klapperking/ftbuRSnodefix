# Overview

---

Simple command-line interface to fix a server-crashing bug in an outdated version of the RefinedStorage Minecraft Mod.

**The bug:** 
* RefinedStorage NodeRecollection of a given block is persisted when the block is destroyed.
* When placing a different RS block at that location, functions of the previously existing block are called
* This causes a crash because the new block does not support these functions

**Fix:** Compare node-recollection at all locations with the real blocks - If not matching, remove the node to prevent future-crash

1. Get all nodes in a given coordinate range
2. Get the block data from minecraft region files
3. Compare blocks and remove nodes when needed

---
### Example Usage

`main.py -s 120 530 -e 200 540`

Given two (x,z) coordinate pairs, checks all blocks in-between (from y 0-256).

Create a new refinedstorage_nodes.dat file with erroring nodes removed

Requires relevant minecraft region files and a refinedstorage node file.
