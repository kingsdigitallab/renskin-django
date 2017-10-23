// Main
require([
    'requirejs',
    'jquery',
    'cookie',
    'ga'
], function(r, $) {
    'use strict';
    $(document).ready(function() {

        // Fix search button
        $('body').on('click', '.searchbutton', function(event) {   

            if ($('#searchright').css('opacity') !== '0') {
                event.preventDefault();
                event.stopPropagation();
                $(this).parent().submit();
            }
        });

        $.scrollTo = $.fn.scrollTo = function(x, y, options) {
            if (!(this instanceof $)) return $.fn.scrollTo.apply($('html, body'), arguments);
            options = $.extend({}, {
                gap: {
                    x: 0,
                    y: 0
                },
                animation: {
                    easing: 'swing',
                    duration: 600,
                    complete: $.noop,
                    step: $.noop
                }
            }, options);
            return this.each(function() {
                var elem = $(this);
                elem.stop().animate({
                    scrollLeft: !isNaN(Number(x)) ? x : $(y).offset().left + options.gap.x,
                    scrollTop: !isNaN(Number(y)) ? y : $(y).offset().top + options.gap.y
                }, options.animation);
            });
        };

        var aChildren = $(".sidebar-nav li").children();
        var aArray = [];
        for (var i = 0; i < aChildren.length; i++) {
            var aChild = aChildren[i];
            var ahref = $(aChild).attr('href');
            aArray.push(ahref);
        }

        $(window).scroll(function() {
            var windowPos = $(window).scrollTop();
            var windowHeight = $(window).height();
            var docHeight = $(document).height();
            for (var i = 0; i < aArray.length; i++) {
                var theID = aArray[i];
                var divPos = $(theID).offset().top;
                var divHeight = $(theID).height();

                if (windowPos >= divPos -10 && windowPos <= (divPos + divHeight)) {
                    $("a[href='" + theID + "']").addClass("name-active");
                } else {
                    $("a[href='" + theID + "']").removeClass("name-active");
                }
            }
            if (windowPos + windowHeight == docHeight) {
                if (!$(".sidebar-nav li:last-child a").hasClass("name-active")) {
                    var navActiveCurrent = $(".name-active").attr("href");
                    $(".sidebar-nav li:last-child a").addClass("name-active");
                }
            }
        });
        $(".sidebar-nav a").click(function(evn) {
            evn.preventDefault();
            $('html,body').scrollTo(this.hash, this.hash);
        });
    });
});