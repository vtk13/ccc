require.config({
    "baseUrl": "/",
    "paths": {
        "jquery": "static/assets/jquery",
        "bootstrap": "static/assets/bootstrap/js/bootstrap.min",
        "selectize": "static/assets/selectize/selectize"
    },
    "shim": {
        "bootstrap": {
            "deps": [
                "jquery"
            ]
        },
        "selectize": {
            "deps": [
                "jquery"
            ]
        }
    }
});

require(['jquery', 'bootstrap', 'selectize'], function($, bs) {
    $('select[name=good]').add('select[name=parent]').selectize({
        valueField: 'id',
        labelField: 'title',
        searchField: ['bar_code', 'title'],
        options: [],
        create: false,
        load: function(query, callback) {
            $.ajax({
                url: '/ajax/goods/' + encodeURIComponent(query),
                type: 'GET',
                dataType: 'json',
                error: function() {
                    callback();
                },
                success: function(res) {
                    callback(res.goods);
                }
            });
        }
    });

    $('select[name=shop]').selectize({
        valueField: 'id',
        labelField: 'title',
        searchField: 'title',
        options: [],
        create: false,
        load: function(query, callback) {
            $.ajax({
                url: '/ajax/shops/' + encodeURIComponent(query),
                type: 'GET',
                dataType: 'json',
                error: function() {
                    callback();
                },
                success: function(res) {
                    callback(res.shops);
                }
            });
        }
    });
});
