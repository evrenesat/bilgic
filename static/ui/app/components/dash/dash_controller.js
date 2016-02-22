angular.module('bilgic.dash', ['ngAnimate'])
    .controller('DashController', function ($animate) {
        $animate.enabled(false);
    });