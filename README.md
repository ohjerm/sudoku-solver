# sudoku-solver
A simple bruteforce sudoku solver I threw together in 3 hours and 34 minutes-ish.

## What does it do?

It solves a sudoku puzzle.

## How does it work?

The program asks for a string. This string should be 9 space-separated 9-digit numbers. Some examples below:

```
308900210 049020863 000008000 007000009 800795006 400000700 000100000 574080620 032006908
910700000 032609080 007080900 086030170 300000006 051020840 009050300 020301490 000002061

080100507 000047093 300080160 060203000 800000006 000408070 038050004 450870000 906004080
804002030 270030500 065410000 000509070 007000300 040301000 000043180 001080053 030100607

400300006 009500042 000000800 080070200 074000160 002090030 008000000 140003700 600004003
700000036 020013900 000760080 870000000 000402000 000000057 080029000 009380040 610000008

950040000 007001380 008000000 700560000 040102090 000034002 000000900 013600500 000080017  # this will not work
```

## What are the limitations?

Currently, it cannot solve sudokus that require a guess. I tested it on puzzles from [websudoku](https://www.websudoku.com/) and as soon as I chose the "evil" difficulty, it gave up.

## What is coming up?

Well, two things are missing:
1. The ability to solve "guesswork" puzzles, and
2. The generator. It doesn't work.
3. The way to input a sudoku puzzle is tedious and should be fixed.

## Contributing

Feel free to open pull requests for anything from refactoring, commenting, module-splitting, feature-improvements or adding new features. 

## Versioning

We'll add some more numbers when some of the major features are implemented.

## Authors

* [Oliver G. Hjermitslev](https://github.com/ChaiKnight)

## License

Licensed under the MIT license. See the LICENSE.txt for details.

## Acknowledgements

Shout out to you if you saw this and thought "I wanna contribute" and then you did.
