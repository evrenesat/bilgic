'use strict';

angular.module('bilgic.play', [])
    .controller('PlayController', function (GameService, $routeParams) {
        GameService.createGame($routeParams.id);
    });