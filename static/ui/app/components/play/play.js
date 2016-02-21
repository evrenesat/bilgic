'use strict';

angular.module('bilgic.play', [])
    .controller('PlayController', function ($scope, GameService, $routeParams, Client, Utilities) {
        Client.getGame($routeParams.key, $scope);
        // game key defined in getGame func in gameService
        $scope.$watch('game', function () {
            GameService.createGame($scope.game);
        });
    });