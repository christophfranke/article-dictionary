from utils.mongo_external import get_collection

def slugify(title):
    return title.lower().replace(' ', '-')[:50]


def migrate_article():
	collection = get_collection('articles')
	articles = collection.find()
	for article in articles:
		if not 'slug' in article:
			article['slug'] = slugify(article['name'])
			article['title'] = article.pop('name')
			collection.replace_one({'_id': article['_id']}, article)

	print('Article Migration complete!')

def clear_slug_prefix():
	collection = get_collection('articles')
	articles = collection.find()
	for article in articles:
		if article['slug'].startswith('/articles/'):
			article['slug'] = article['slug'][10:]
			collection.replace_one({'_id': article['_id']}, article)

	print('Article Slug Prefix Removal complete!')

def migrate():
	clear_slug_prefix()