if type jq > /dev/null 2>&1; then
	for f in wordpages/*.json
	do
		replaced_wordpages=${f/wordpages\//}
		echo "$(jq --arg file "$f" '.["entry_data"].TagPage[0].tag.media.count' "$f") ${replaced_wordpages/.json/}"
	done
else
	echo "Please install jq: https://stedolan.github.io/jq/"
fi
