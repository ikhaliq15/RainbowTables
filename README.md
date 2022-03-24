# Rainbow Tables
A prototype implementation of a rainbow table.

A [Rainbow Table](https://en.wikipedia.org/wiki/Rainbow_table) is a data structure to improve efficency of using precomputed lookup tables to find the preimages of functions. In particular, rainbow tables are used to reverse hash functions like SHA-1, MD5, etc... Rainbow tables are useful when we have a specific subset of values that we want to precompute our table over (i.e: 8 character alphanumeric string). The rainbow table has parameters that enable a user to choose their desired balance between storage of the table and lookup time within the table.

<p align="center">
  <img alt="rainbow table" width="700" src="https://user-images.githubusercontent.com/6558567/159884413-d741f3d8-7d11-4728-b80d-4a6111e3186e.png">
</p>

This implementation is done in Python as a prototype. As such, it lacks many optimizations as well as the natural speed up of using a lower level language. However, this tradeoff was made for learning purposes as the main goal of implementing the rainbow table was to get a better understanding of the technique, rather than squeeze out optimal performance. It focuses on the MD5 hash but could easily be extended to any other hash function.

## Features
Some features included in this prototype:
* Ability to tune parameters such as chain lengths and number of chains to have greater control over storage size and search time.
* Ability to set a custom alphabet set and a custom preimage string length.
* Ability to save generated rainbow tables as files and load them later to allow for reuse for future hash lookups.

## Goals
Some goals for future work:
* Add multiple chain generation phases to reduce merged chains from wasting time and space.
* Add optimizations to reduction functions to decrease runtime.
* Write the project in a lower level language such as Rust to try and push performance.
