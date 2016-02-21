'use strict';

// Declare app level module which depends on views, and components
angular.module('bilgic', [
    'ngRoute',
    'ngAnimate',
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
            .when('/games/edit/:key', {
                templateUrl: 'components/games/addEditGame.html',
                controller: 'GamesEditController'
            })
            .when('/play/:key', {
                templateUrl: 'components/play/play.html',
                controller: 'PlayController'
            })
            .otherwise({redirectTo: '/games'});
    }])
    .config(['$httpProvider', function ($httpProvider) {
        // to send cookies CORS
        //$httpProvider.defaults.withCredentials = true;
    }])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.interceptors.push(function ($q, $rootScope, $location, $timeout, $log) {
            return {
                'request': function (config) {
                    if (config.method === "POST") {
                        config.headers["Content-Type"] = "text/plain";
                    }
                    return config;
                },
                'response': function (response) {
                    return response;
                },
                'responseError': function (rejection) {
                    return rejection
                }
            };
        });
    }])
    .service('Settings', function () {
        return {'api_url': 'http://192.168.1.5:8080/'}
    });