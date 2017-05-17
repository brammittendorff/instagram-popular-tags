# How to use

Download every word from wordlist

```
python download_tags_to_json.py -s wordlist.txt
```

Show latest 100 results sorted by tag amount

```
./show.sh | sort -nr | head -n 100
```

To watch the process happening in a other terminal

```
watch -d -n 1 './show.sh | sort -nr | head -n 100'
```
