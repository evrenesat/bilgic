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
            var myCountdownSeconds, marker, tileset, map, layer, currentTilePosition;
            var masterCounter = 0;
            var squareCounter = 0;
            var first, second;

            var gameContent = gameService.getGame(gameId);

            var game = new BPhaser.Game("100%", "100%",
                BPhaser.AUTO, '', {preload: preload, create: create, update: update, render: render});

            function preload() {
                //game.load.tilemap('matching', 'components/phaser_tiles.json', null, Phaser.Tilemap.TILED_JSON);

                // load images in preload
                // add expression if content type is image

                angular.forEach(gameContent.pictures, function (value, key) {
                    game.load.image(value.pic_id, value.picture);
                });
            }

            function create() {
                //map = game.add.tilemap('matching');
                //
                //map.addTilesetImage('Desert', 'tiles');
                //
                ////tileset = game.add.tileset('tiles');
                //
                //layer = map.createLayer('Ground');//.tilemapLayer(0, 0, 600, 600, tileset, map, 0);
                //
                ////layer.resizeWorld();
                //marker = game.add.graphics();
                //marker.lineStyle(2, 0x00FF00, 1);
                //marker.drawRect(0, 0, 100, 100);


                var anchor = [0, 0];
                angular.forEach(gameContent.pictures, function (value, key) {
                    var img = game.add.sprite(game.world.centerX, game.world.centerY, value.pic_id);
                    img.anchor.setTo(anchor[0], anchor[1]);
                    img.inputEnabled = true;
                    img.events.onInputDown.add(match, this);
                    anchor = anchor.map(function (x) {
                        return x + 0.5;
                    })
                });
            }

            function update() {
            }

            function match(sprite, pointer){
                console.log(first === sprite.key);
                first = sprite.key;
            }

            function render() {
                game.debug.text('First: ' + first, 900, 15, 'rgb(0,255,0)');
                game.debug.text('Matched Pairs: ' + masterCounter, 900, 35, 'rgb(0,255,255)');
            }
        };
        return gameService;
    });