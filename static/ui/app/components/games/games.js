'use strict';

angular.module('bilgic.games', [])
    .controller('GamesController', function ($scope, $location, GameService) {
        GameService.getGames()
            .then(function (data) {
                $scope.games = data.data;
            });
    })
    .controller('GameEditController', function ($scope, $location, GameService) {
        // get or create games
    });