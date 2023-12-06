'use strict';
$(function() {
    let cookie = Cookies;
    if (!cookie.get('renskin-cookie')) {
      $("#cookie-disclaimer").removeClass('hide');
    }
    // Set cookie
    $('#cookie-disclaimer .closeme').on("click", function() {
      cookie.set('renskin-cookie', 'renskin-cookie-set', {
          expires: 30
      });
    });

    $('.closeme').bind("click", function () {
        $('#cookie-disclaimer').addClass("hide");
        return false;
    });
});
