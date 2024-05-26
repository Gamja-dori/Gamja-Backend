FROM docker.elastic.co/elasticsearch/elasticsearch:7.15.2

RUN if ! [ -d "/usr/share/elasticsearch/plugins/analysis-nori" ]; then \
    elasticsearch-plugin install analysis-nori; \
    fi