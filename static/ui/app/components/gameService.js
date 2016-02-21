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
            var point, anchor;
            var first, second; // for matchings
            var firstSprite, secondSprite;
            var isSecond = false;
            var clickAudio, winAudio;
            var text = null;
            var grd;

            // get game from localStorage or remote api
            var gameContent = gameService.getGame(gameId);

            window.WebFontConfig = {

                //  'active' means all requested fonts have finished loading
                //  We set a 1 second delay before calling 'createText'.
                //  For some reason if we don't the browser cannot render the text the first time it's created.
                //active: function() { game.time.events.add(Phaser.Timer.SECOND, startGame, this); },

                //  The Google Fonts we want to load (specify as many as you like in the array)
                google: {
                    families: ['Caveat+Brush::latin,latin-ext']
                }

            };

            var game = new BPhaser.Game("100%", "100%",
                BPhaser.AUTO, '', {preload: preload, create: create, update: update, render: render});

            function preload() {
                game.load.script('webfont', '//ajax.googleapis.com/ajax/libs/webfont/1.4.7/webfont.js');
                game.load.audio('click', 'asset/button_push.mp3');
                game.load.audio('win', 'asset/win.mp3');
                // load images in preload
                // add expression if content type is image
                angular.forEach(gameContent.pictures, function (value, key) {
                    game.load.image(value.pic_id, value.picture);
                });
            }

            function create() {

                game.stage.backgroundColor = '#0072bc';
                clickAudio = game.add.audio('click');
                winAudio = game.add.audio('win');
                game.sound.setDecodedCallback([ clickAudio, winAudio ], audioCB, this);

                point = new Phaser.Point(30, 30);

                anchor = [0, 0];
                gameContent.pictures = shuffle(gameContent.pictures);
                angular.forEach(gameContent.pictures, function (value, key) {
                    var img = game.add.sprite(point.x, point.y, value.pic_id);
                    img.anchor.setTo(anchor[0], anchor[1]);
                    img.inputEnabled = true;
                    img.events.onInputDown.add(match, this);
                    img.scale.setTo(0.7, 0.7);
                    anchor = calcAnchor(anchor);
                });
            }

            function calcAnchor(anchor, matrix) {
                // matrix need to be like 4x4 or 5x5
                var mtrx = ((matrix || '4x4').split('x')).map(function (x) {
                    return 1.3*(-(Number(x))+1); // need to be index
                });
                var newAnchor = anchor;

                if (anchor[0] === mtrx[0]) {
                    newAnchor[1] -= 1.3;
                    newAnchor[0] = 1.3;
                }
                newAnchor[0] = anchor[0] - 1.3;
                return newAnchor;
            }

            function shuffle(array) {
                var m = array.length, t, i;
                while (m) {
                    i = Math.floor(Math.random() * m--);
                    t = array[m];
                    array[m] = array[i];
                    array[i] = t;
                }
                return array;
            }

            function audioCB() {}

            function update() {}

            function match(sprite, pointer) {
                clickAudio.play();
                if (first === sprite.key) {
                    masterCounter++;
                    winAudio.play();
                    firstSprite.destroy();
                    sprite.destroy();
                    startGame();
                }
                if (!isSecond) {
                    first = sprite.key;
                    firstSprite = sprite;
                    isSecond = !isSecond;
                } else {
                    isSecond = !isSecond;
                }

            }

            var debugText;
            function render() {
                debugText = game.debug.text('Matched Pairs: ' + masterCounter, 820, 65, 'rgb(100,255,255)');
                //debugText.font = 'Caveat Brush';
                //debugText.fontSize = 60;
            }

            function startGame() {

                text = game.add.text(game.world.centerX, game.world.centerY, "- bilgiç -\nstart game\noyuna başla");
                text.anchor.setTo(0.5);

                text.font = 'Caveat Brush';
                text.fontSize = 60;

                //  x0, y0 - x1, y1
                grd = text.context.createLinearGradient(0, 0, 0, text.canvas.height);
                grd.addColorStop(0, '#8ED6FF');
                grd.addColorStop(1, '#004CB3');
                text.fill = grd;

                text.align = 'center';
                text.stroke = '#000000';
                text.strokeThickness = 2;
                text.setShadow(5, 5, 'rgba(0,0,0,0.5)', 5);

                text.inputEnabled = true;
                text.input.enableDrag();

                text.events.onInputOver.add(over, this);
                text.events.onInputOut.add(out, this);

            }

            function out() {

                text.fill = grd;

            }

            function over() {

                text.fill = '#ff00ff';

            }
        };
        return gameService;
    });