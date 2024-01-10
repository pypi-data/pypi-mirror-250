# ChangeLog

## 2024 Jan 9 - v0.0.1

- first release
- full Python, using dataclasses with slots
- has the S heurisitic implemented
- one single API endpoint exposed: `exact_covers`
  which returns a generator over all solutions
- tested on a small number of problems
- approx. 20 times slower than the C version
  on finding the first solution
