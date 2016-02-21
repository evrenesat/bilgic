'use strict';

angular.module('bilgic.games', [])
    .controller('GamesController', function ($scope, $location, GameService) {
        GameService.getGames()
            .success(function (data) {
                $scope.games = data.games;
            });
        $scope.getlevels = function (key) {
            GameService.getGameLevels(key)
                .success(function (data) {
                    $scope.gameLevels = data.levels;
                });
        }
    })
    .controller('GameEditController', function ($scope, $location, GameService) {
        // get or create games
    });