if type jq > /dev/null 2>&1; then
	for f in wordpages/*.json
	do
		echo "$(jq --arg file "$f" '.["entry_data"].TagPage[0].graphql.hashtag.edge_hashtag_to_media.count' "$f") ${f}"
	done
else
	echo "Please install jq: https://stedolan.github.io/jq/"
fi
