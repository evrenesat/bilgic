'use strict';
// todo: load game and content to localstorage
angular.module('bilgic')
    .service('BPhaser', function () {
        return window.Phaser;
    })
    .factory('GameService', function ($http, $timeout, $location, BPhaser, Settings) {
        var gameService = {};
        gameService.games = [];
        gameService.getGames = function () {
            return $http.get(Settings.api_url + 'games')
                .success(function (res) {
                    return res.data;
                });
        };
        gameService.getGameLevels = function (key) {
            return $http.get(Settings.api_url + 'game_levels/' + key)
                .success(function (res) {
                    return res.data;
                });
        };
        gameService.getGame = function (key, scope) {
            if (localStorage.getItem("game_" + key)) {
                scope.game = JSON.parse(localStorage.getItem("game_" + id));
            } else {
                $http.get(Settings.api_url + 'get_level/' + key)
                    .success(function (res) {
                        scope.game = res;
                        localStorage.setItem("game_" + res.key, JSON.stringify(res));
                    });
            }
        };
        gameService.saveGames = function () {

        };
        gameService.createGame = function (gameContent) {
            if(!gameContent) {return;}

            var masterCounter = 0;
            var totalSprites;
            var point, anchor, first, second; // for matchings
            var firstSprite, secondSprite;
            var isSecond = false;
            var clickAudio, winAudio;
            var text, grd, successText, exitText;

            // get game from localStorage or remote api

            var game = new BPhaser.Game("100%", "100%", BPhaser.AUTO, 'play-in', {
                preload: preload,
                create: create,
                update: update,
                render: render
            });

            function preload() {
                game.load.script('webfont', '//ajax.googleapis.com/ajax/libs/webfont/1.4.7/webfont.js');
                game.load.audio('click', 'asset/button_push.mp3');
                game.load.audio('win', 'asset/win.mp3');

                // load images in preload
                // add expression if content type is image
                angular.forEach(gameContent.elements, function (value, key) {
                    game.load.image(value.key, 'data:image/jpg;base64,'+value.content);
                });
            }

            function create() {
                game.stage.backgroundColor = '#26D6D0';
                clickAudio = game.add.audio('click');
                winAudio = game.add.audio('win');
                game.sound.setDecodedCallback([clickAudio, winAudio], audioCB, this);

                point = new Phaser.Point(30, 30);

                anchor = [0, 0];
                gameContent.elements = shuffle(gameContent.elements);
                angular.forEach(gameContent.elements, function (value, key) {
                    var img = game.add.sprite(point.x, point.y, value.key);
                    img.anchor.setTo(anchor[0], anchor[1]);
                    img.inputEnabled = true;
                    img.events.onInputDown.add(match, this);
                    img.scale.setTo(0.7, 0.7);
                    img.angle = parseInt((Math.random() < 0.5 ? 1 : -1) * (Math.random() * (5 - 1)));
                    anchor = calcAnchor(anchor);
                });
                totalSprites = gameContent.elements.length;

                successText = game.add.text(game.world.width-180, 15, "Skor: 0", {font: "50px foo", fill: "#FAF490"});
                successText.anchor.setTo(0, 0);
                exitText = game.add.text(game.world.width-180, game.world.height-100, "Exit", {font: "50px foo", fill: "#FAF490"});
                exitText.anchor.setTo(0, 0);
                exitText.inputEnabled = true;
                exitText.events.onInputDown.add(exitGame, this);
            }

            function calcAnchor(anchor, matrix) {
                // matrix need to be like 4x4 or 5x5
                var mtrx = ((matrix || '2x5').split('x')).map(function (x) {
                    return 1.3 * (-(Number(x)) + 1); // need to be index
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

            function restart() {
                game.state.restart();
                masterCounter = 0;
            }

            function update() {}

            function match(sprite, pointer) {
                clickAudio.play();
                if (first === sprite.key) {
                    masterCounter++;
                    winAudio.play();
                    firstSprite.destroy();
                    sprite.destroy();
                    totalSprites -= 2;
                    if (totalSprites == 0) {
                        restartGame();
                    }
                    successText.setText("Skor: " + masterCounter);
                }
                if (!isSecond) {
                    first = sprite.key;
                    firstSprite = sprite;
                    isSecond = !isSecond;
                } else {
                    isSecond = !isSecond;
                }

            }

            function render() {}

            function restartGame() {
                text = game.add.text(game.world.centerX, game.world.centerY, "- tebrikler -\nrestart game\nyeniden başla");
                text.anchor.setTo(0.5);

                text.font = 'foo';
                text.fontSize = 60;
                //  x0, y0 - x1, y1
                grd = text.context.createLinearGradient(0, 0, 0, text.canvas.height);
                grd.addColorStop(0, '#26DAF9');
                grd.addColorStop(1, '#004CB3');
                text.fill = grd;
                text.align = 'center';
                text.stroke = '#000000';
                text.strokeThickness = 2;
                text.setShadow(5, 5, 'rgba(0,0,0,0.5)', 5);
                text.inputEnabled = true;
                text.events.onInputOver.add(over, this);
                text.events.onInputOut.add(out, this);

                game.input.onDown.add(restart, this);
            }

            function out() {
                text.fill = grd;
            }

            function over() {
                text.fill = '#ff00ff';
            }

            // quit and go to main page

            function exitGame() {
                //document.querySelector('canvas').remove();
                location.hash = '#/games';
            }

        };
        return gameService;
    });