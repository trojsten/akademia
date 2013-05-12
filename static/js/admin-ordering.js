/* Inspired by the snippet at http://djangosnippets.org/snippets/1053/
 */

$(function() {
    var setup_ordering = function() {
        var $inline = $(this);
        var $tbody = $inline.find('tbody');
        var $rows = $tbody.find('tr.form-row');
        var $order_fields = $rows.find('td.field-order');

        if ((!$inline.size()) || ($order_fields.size() !== $rows.size())) {
            // There is no "order" field or no inline at all.
            return;
        }

        $tbody.sortable({
            axis: 'y',
            items: '> tr.form-row',
            update: function() {
                $(this).find('tr.form-row:not(.empty-form)')
                .each(function(i) {
                    $(this)
                    .removeClass('row1').removeClass('row2')
                    .addClass('row' + ((i % 2) + 1))
                    .find('td.field-order input').val(i+1);
                });
            },
        });

        $tbody.find('> tr.form-row').css('cursor', 'move');
    };

    $('div.inline-group > div.tabular').each(setup_ordering);
});
