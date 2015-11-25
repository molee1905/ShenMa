/**
 * Add description here
 *
 * @module: __name__
 * @author __author__
 * @version __version__
 */

(function (fn) {

    'use strict';

    fn['__name__'] = function (opts) {
        
        var scope = this;
        
        function init() {

            bindEvent();
        }

        function bindEvent() {
            scope.on('click', function () {

            });
        }

        init();
    };

})(sm.fn);

