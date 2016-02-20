'use strict';
// todo: load game and content to localstorage
angular.module('bilgic')
    .service('BPhaser', function () {
        return window.Phaser;
    })
    .factory('GameService', function ($http, $timeout, BPhaser) {
        var gameService = {};
        gameService.games = [];
        gameService.getGames = function () {
            return $http.get('components/games.json')
                .success(function (res) {
                    return res.data;
                });
        };
        gameService.getGame = function (id) {
            if (localStorage.getItem("game_" + id)) {
                return JSON.parse(localStorage.getItem("game_" + id));
            } else {
                var game;
                $http.get('components/game.json')
                    .success(function (res) {
                        localStorage.setItem("game_" + res._id, JSON.stringify(res));
                        game = res;
                    });
                return game;
            }
        };
        gameService.saveGames = function () {

        };
        gameService.createGame = function (gameId) {
            var gameContent = gameService.getGame(gameId);

            var game = new BPhaser.Game(960, 720,
                BPhaser.AUTO, '', {preload: preload, create: create, update: update});

            function preload() {
                // add expression if content type is image
                angular.forEach(gameContent.pictures, function (value, key) {
                    game.load.image(value.pic_id, value.picture);
                });
            }

            function create() {
                var anchor = [0.1, 0.1];
                angular.forEach(gameContent.pictures, function (value, key) {
                    var img = game.add.sprite(game.world.centerX, game.world.centerY, value.pic_id);
                    img.anchor.setTo(anchor[0], anchor[1]);
                    anchor = anchor.map(function (x) {
                        return x + 0.1;
                    })
                });

                game.input.onDown.add(match, this);
            }

            function update() {
            }

            function match(item){
                console.log(item);
            }
        };
        return gameService;
    });