# Magikarp
Answer quick questions like "What was the plural of _exempel_?" without going to [svenska.se](https://svenska.se).

Put together in one evening to learn how to use the [Karp API](https://spraakbanken4.it.gu.se/karp/v7/) and to encourage myself to check that I'm inflecting stuff properly more often.
Exceptions are unhandled because I had other priorities. 

## Usage

```
python magikarp.py LEMMA [FEATS...]
```

where:

- `LEMMA` is the dictionary form of the word, e.g. "exempel"
- `FEATS` is a (non-exhaustive) set of morphological features, e.g. "pl def"
