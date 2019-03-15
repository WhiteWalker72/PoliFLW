from src.persistence import sources_service
import src.api.rest_utils as rest_utils


def get_sources():
    sources = sources_service.find_sources()
    for article in sources:
        article.pop('_id', None)
    return sources


def add_source(url):
    source_found = sources_service.find_source(url)
    if source_found:
        return rest_utils.get_error(409, 'source with url ' + url + ' already exists')

    sources_service.add_source({'url': url})
    source_found = sources_service.find_source(url)
    source_found.pop('_id', None)
    return source_found


def delete_source(url):
    source_found = sources_service.find_source(url)

    if not source_found:
        return rest_utils.get_error(404, 'source with url ' + url + ' does not exists')

    sources_service.delete_source(url)
    return '', 204


