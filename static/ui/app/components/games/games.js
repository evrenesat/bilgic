'use strict';

angular.module('bilgic.games', [])
    .controller('GamesController', function ($scope, $location, GameService, Client, Utilities) {
        Client.getGames()
            .success(function (data) {
                $scope.games = data.games;
            });
        $scope.getlevels = function (key) {
            Client.getGameLevels(key)
                .success(function (data) {
                    $scope.gameLevels = data.levels;
                });
        };
        $scope.removeLevels = function () {
            delete $scope.gameLevels;
        };
    })
    .controller('GameEditController', function ($scope, $location, $timeout, Editor, Client) {
        Client.getGames().success(function (res) {
            $scope.games = res.games;
        });
        $scope.page = 1;
        $scope.nextPage = function (page) {
            $scope.search_results = 0;
            $scope.page += 1;
            Editor.search_images($scope.kw + '/' + page)
                .success(function (data) {
                    $scope.search_results = data.results;
                });
        };
        $scope.search_images = function () {
            $scope.search_results = 0;
            Editor.search_images($scope.kw+'/1')
                .success(function (data) {
                    $scope.search_results = data.results;
                });
        };
        $scope.selected = [];
        $scope.selected_src = {};
        $scope.selectToggle = function (item) {
            if ($scope.isSelected(item.currentTarget.id)) {
                $scope.selected.splice($scope.selected.indexOf(item.currentTarget.id), 1);
                delete $scope.selected_src[item.currentTarget.id];
            } else {
                $scope.selected.push(item.currentTarget.id);
                $scope.selected_src[item.currentTarget.id] = {content: item.currentTarget.src};
            }
        };
        $scope.isSelected = function (id) {
            return $scope.selected.indexOf(id) > -1;
        };
        $scope.set_level = function () {
            Editor.set_level($scope.levelName, $scope.selected_src, $scope.selected_game)
                .success(function (data) {
                    $location.path('#/games/' + data.new_level_id);
                });
        };
    });