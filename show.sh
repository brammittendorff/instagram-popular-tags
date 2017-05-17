for f in wordpages/*.json
do
	echo "$(jq --arg file "$f" '.["entry_data"].TagPage[0].tag.media.count' "$f") ${f}"
done
