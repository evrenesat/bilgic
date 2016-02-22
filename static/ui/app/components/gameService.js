'use strict';
// todo: load game and content to localstorage
angular.module('bilgic')
    .service('BPhaser', function () {
        return window.Phaser;
    })
    .factory('GameService', function ($http, $timeout, $location, BPhaser, Utilities, Preload) {
        var gameService = {};
        gameService.createGame = function (gameContent) {
            if(!gameContent) {return;}

            var masterCounter = 0, totalSprites, point, anchor, first, second;
            var firstSprite, secondSprite;
            var isSecond = false;
            var clickAudio, winAudio;
            var text, grd, successText, exitText;

            // get game from localStorage or remote api
            var game = new BPhaser.Game("100%", "100%", BPhaser.CANVAS, 'play-in', {
                preload: preload,
                create: create,
                update: update,
                render: render
            });

            function preload() {
                Preload.preload(game, gameContent);
            }

            function create() {
                game.add.tileSprite(0, 0, window.innerWidth, window.innerHeight, 'bg2');
                clickAudio = game.add.audio('click');
                winAudio = game.add.audio('win');
                game.sound.setDecodedCallback([clickAudio, winAudio], audioCB, this);
                //var blurX = game.add.filter('BlurX');
                //var blurY = game.add.filter('BlurY');
                point = new Phaser.Point(30, 30);

                anchor = [0, 0];
                angular.forEach(gameContent.elements, function (value, key) {
                    var shadow = game.add.sprite(point.x, point.y, value.key);
                    var img = game.add.sprite(point.x, point.y, value.key);
                    img.shadow = shadow;
                    shadow.anchor.setTo(anchor[0]-0.05, anchor[1]-0.05);
                    shadow.tint = 0x000000;
                    shadow.alpha = 0.3;
                    shadow.width = 100;
                    shadow.height = 100;

                    //shadow.filters = [blurX, blurY];
                    img.anchor.setTo(anchor[0], anchor[1]);
                    img.inputEnabled = true;
                    img.events.onInputDown.add(match, this);
                    //img.scale.setTo(0.7, 0.7);
                    img.width = 100;
                    img.height = 100;
                    var angle = parseInt((Math.random() < 0.5 ? 1 : -1) * (Math.random() * (5 - 1)));
                    if(typeof window.orientation == 'undefined'){
                        img.angle = angle;
                        shadow.angle = angle;
                    }
                    anchor = Utilities.calcAnchor(anchor);
                });
                totalSprites = gameContent.elements.length;

                successText = game.add.text(game.world.width-220, 15, "Score: 0 ", {font: "50px foo", fill: "#FAF490"});
                successText.alpha = 0.5;
                successText.setShadow(5, 5, 'rgba(0,0,0,0.5)', 15);
                successText.anchor.setTo(0, 0);
            }

            function audioCB() {}

            function restart() {
                game.state.restart();
                masterCounter = 0;
            }

            function update() {}

            function match(sprite, pointer) {
                clickAudio.play();

                if (first === sprite.key && firstSprite.position != sprite.position) {

                    masterCounter++;
                    winAudio.play();
                    firstSprite.shadow.destroy();
                    firstSprite.destroy();
                    sprite.shadow.destroy();
                    sprite.destroy();
                    totalSprites -= 2;
                    if (totalSprites == 0) {
                        restartGame();
                    }
                    successText.setText("Score: " + masterCounter);
                }else {
                    if (!isSecond) {
                        first = sprite.key;
                        firstSprite = sprite;
                        sprite.alpha = 0.6;
                        sprite.tint = 0xf0f000;
                    } else {
                        first = null;
                        firstSprite.alpha = 1;
                        firstSprite.tint = 0xFFFFFF;
                        sprite.tint = 0xFFFFFF;
                        sprite.alpha = 1;
                    }
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
                location.hash = '#/games';
            }

        };
        return gameService;
    });
