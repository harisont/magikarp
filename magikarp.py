import urllib.request
from urllib.parse import quote
import json
import argparse
import yaml

if __name__ == "__main__":
  with open("config.yaml") as config:
    config = yaml.safe_load(config)

  parser = argparse.ArgumentParser(description='''
Answer quick questions like what was the plural of "exempel" without going to 
svenska.se''')
  parser.add_argument('lemma', help='the dictionary form of the word')
  parser.add_argument('feats', help='a list of morpho features', nargs='*')
  args = parser.parse_args()

  lemma = args.lemma
  query_feats = set(args.feats)
  ignored_feats = set(config["ignores"]["pos"]) - query_feats
  ignored_pos = set(config["ignores"]["pos"])

  saldom_string = urllib.request.urlopen(
    "{}/query/saldom?q=equals|baseform|%22{}%22&size=10" 
    .format(config["karp_url"], quote(lemma))).read()
  saldom_dict = json.loads(saldom_string)

  # filter hits by POS and feats
  hits = [hit for hit in saldom_dict["hits"] 
          if hit["entry"]["partOfSpeech"] not in ignored_pos and
          # use input feats for partial disambiguation
          all([feat in " ".join([row["msd"] 
                                 for row in hit["entry"]["inflectionTable"]]) 
                                 for feat in query_feats])]
  tot = len(hits)
  if tot == 0:
    print("inga resultat!")
    exit(0)
  n = 0

  # when disambiguation is not possible, ask the user to choose by POS
  if tot > 1:
    for (i,hit) in enumerate(hits):
      entry = hit["entry"]
      pos = entry["partOfSpeech"]
      print('{}. {} ({})'.format(i + 1, lemma, pos))
    n = int(input("\nChoose one: ")) - 1
  hit = hits[n] 
  table = hit["entry"]["inflectionTable"]

  # show relevant rows of the selected inflection table
  for row in table:
    msd_feats = row["msd"].split()
    if (all([feat in msd_feats for feat in query_feats]) and 
        not any([feat in msd_feats for feat in ignored_feats])):
      print("{: >30}: {: <15}".format(row["msd"], row["writtenForm"]))
