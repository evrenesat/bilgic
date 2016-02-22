angular.module('bilgic')
.factory('Utilities', function (Settings) {
    var utilities = {};
    utilities.calcAnchor = function(anchor, matrix) {
        // matrix need to be like 4x4 or 5x5
        //matrix =
        var mtrx = ((matrix || Settings.default_matrix).split('x')).map(function (x) {
            return 1.3 * (-(Number(x)) + 1); // need to be index
        });
        var newAnchor = anchor;

        if (anchor[0] === mtrx[0]) {
            newAnchor[1] -= 1.3;
            newAnchor[0] = 1.3;
        }
        newAnchor[0] = anchor[0] - 1.3;
        return newAnchor;
    };
    utilities.shuffle = function(array) {
        var m = array.length, t, i;
        while (m) {
            i = Math.floor(Math.random() * m--);
            t = array[m];
            array[m] = array[i];
            array[i] = t;
        }
        return array;
    };
    utilities.calcImageSize = function(){
        Settings.default_matrix.split('x')
    }
    utilities.gcd = function(a, b) {
        if ( ! b) {
            return a;
        }
        return gcd(b, a % b);
    };
    return utilities;
});
