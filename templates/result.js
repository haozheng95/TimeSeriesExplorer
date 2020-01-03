{% if problem_category == 1 %}
window.jsonpCb && window.jsonpCb({
    problemCategory: {{ problem_category | safe }},
    dimensionInfo: {{ dimension_info | safe }},
    featureInfo: {{ feature_info | safe }},
    part1: {{ problem_desc | safe }},
    part2List: {{ feature_desc_list | safe }},
    part3: {
        matrix: {{ features_rel | safe }},
        featureList: {{ feature_list | safe }}
    },
    part4: {
        featureTargetRel: {{ features_target_rel | safe }}
    },
});
{% else %}
window.jsonpCb && window.jsonpCb({
    problemCategory: {{ problem_category | safe }},
    dimensionInfo: {{ dimension_info | safe }},
    featureInfo: {{ feature_info | safe }},
    part1: {
        histogramList: {{ problem_desc_histogram_list | safe }},
        descStatSum: {{ problem_desc_descriptive_statistics_summary | safe }},
        skewness: {{ problem_desc_skewness | safe }},
        kurtosis: {{ problem_desc_kurtosis | safe }},
    },
    part2List: {{ feature_desc_list | safe }},
    part3: {
        matrix: {{ features_rel | safe }},
        featureList: {{ feature_list | safe }}
    },
    part4: {
        featureTargetRel: {{ features_target_rel | safe }}
    },
});
{% endif %}
