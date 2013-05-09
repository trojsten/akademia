/*
 * Star ratings for Django RadioSelect widgets.
 *
 * Copyright (c) 2013 Michal Petrucha <michal.petrucha@ksp.sk> Modified to
 * match the Django RadioSelect template and updated to use SVG.
 * Copyright (c) 2011 Tomi Belan <tomi.belan@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

(function($) {
    var cancelText = "Zruš odpoveď";

    $('html').addClass('with-stars-js');

    var trim = function(str) {
        // remove all whitespace from str's beginning and end
        return str.replace(/^\s*|\s*$/g, "");
    }

    var setup_stars = function() {
        var $question = $(this);
        var $ul = $question.find('ul').not('.errorlist');
        var $none_option = $question.find('.stars[type="radio"][value=""]');
        var $options = $question.find('.stars[type="radio"]').not($none_option);
        if (!($ul.length == 1 && $none_option.length == 1 && $options.length > 0)) {
            return;
        }
        var $labels = $options.parent();

        $ul.addClass("hidden-stars-radios");

        var $container = $('<div />', {
            'class': 'stars-container',
        });
        $container.insertAfter($ul);
        for (var i = 0; i < $options.length; i++) {
            var $span = $('<span />', {
                'class': 'star',
                'title': trim($labels.eq(i).text()),
                'data': {'id': i},
            }).append($('<svg />', {
                'viewBox': "-10 -10 259 247",
            }).prepend($('<polygon />', {
                'points': "119,0 148,86 238,86 166,140 192,226 119,175 46,226 72,140 0,86 90,86",
            })));
            // The following hack is here because while jQuery manages
            // to add the necessary SVG elements to the DOM, the browser
            // won't pick them up since they aren't HTML; this forces
            // the browser to reparse the whole tree correctly.
            $span.html($span.html());
            $container.append($span);
        }
        var $span = $('<span />', {
            'class': 'cancel',
            'title': cancelText,
        }).append($('<svg />', {
            'viewBox': "-2 -3 14 14",
        }).append($('<polygon />', {
            'points': "0,2 2,0 5,3 8,0 10,2 7,5 10,8 8,10 5,7 2,10 0,8 3,5",
        })));
        // Same hack as above.
        $span.html($span.html());
        $container.append($span);
        var $cancel = $container.find('.cancel');
        var $stars = $container.find('.star');

        var redraw = function() {
            var active = -1;
            for (var i = 0; i < $options.length; i++) {
                if ($options[i].checked) active = i;
            }
            for (var i = 0; i < $stars.length; i++) {
                $stars.eq(i).toggleClass('active', i <= active).removeClass('hover');
            }
            $container.removeClass('cancel-hover');
            $cancel.toggle(active != -1);
        };
        var redraw_hover = function() {
            redraw();
            var hover = $(this).data('id');
            for (var i = 0; i < $stars.length; i++) {
                $stars.eq(i).toggleClass('hover', i <= hover);
            }
        }

        $options.add($none_option).on("change", redraw);
        $stars.on({
            'mouseover': redraw_hover,
            'mouseout': redraw,
            'click': function() {
                $options[$(this).data('id')].checked = true;
                redraw();
            },
        });
        $cancel.on({
            'mouseover': function() {
                $container.addClass('cancel-hover');
            },
            'mouseout': redraw,
            'click': function() {
                $none_option[0].checked = true;
                redraw();
            },
        });

        redraw();
    };

    $(function() {
        $('.poll_question').each(setup_stars);
    });
})(jQuery);
