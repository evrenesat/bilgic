'use strict';

// Declare app level module which depends on views, and components
angular.module('bilgic', [
    'ngRoute',
    'bilgic.games',
    'bilgic.play'
    //'myApp.version'
]).config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/games', {
            templateUrl: 'components/games/games.html',
            controller: 'GamesController'
        })
        .when('/games/add', {
            templateUrl: 'components/games/addEditGame.html',
            controller: 'GameEditController'
        })
        .when('/games/edit/:id', {
            templateUrl: 'components/games/addEditGame.html',
            controller: 'GamesEditController'
        })
        .when('/play/:id', {
            templateUrl: 'components/play/play.html',
            controller: 'PlayController'
        })
        .otherwise({redirectTo: '/games'});
}]);