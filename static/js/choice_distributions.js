$(function() {
    var get_column = function($table, index, f) {
        if (f === undefined) {
            f = function(v) {return v;};
        }
        var result = [];
        $table.find('tr').each(function() {
            result.push(f($(this).children().eq(index).text()));
        });
        return result;
    };

    var setup_chart = function() {
        var $question = $(this);
        var $tbody = $question.find('tbody');

        var $container = $('<div />', {
            'class': 'choice-dist-container',
        });
        $question.before($container);

        var settings = {
            'chart': {
                'type': 'bar',
            },
            'xAxis': {
                'categories': get_column($tbody, 0),
            },
            'yAxis': {
                'allowDecimals': false,
                'min': 0,
                'labels': {
                    'overflow': 'justify',
                },
                'title': {
                    'text': null,
                },
            },
            'plotOptions': {
                'bar': {
                    'dataLabels': {
                        'enabled': true,
                    },
                    'groupPadding': 0,
                },
            },
            'credits': {
                'enabled': false,
            },
            'series': [{
                'data': get_column($tbody, 1, Number),
            }],
            'legend': {
                'enabled': false,
            },
            'tooltip': {
                'enabled': false,
            },
            'title': {
                'text': null,
            },
        };

        $container.highcharts(settings);
    }

    $('html').addClass('with-highcharts');
    $('.poll_options_result').each(setup_chart);
});
