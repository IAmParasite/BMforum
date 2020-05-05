# 搜索设置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': '',
        'INDEX_NAME': 'hellodjango_blog_tutorial',
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'