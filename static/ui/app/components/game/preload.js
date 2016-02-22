angular.module('bilgic')
.factory('Preload', function () {
    var game = {};
    game.preload = function(game, gameContent) {
        game.load.audio('click', 'asset/button_push.mp3');
        game.load.audio('win', 'asset/win.mp3');
        //game.load.script('filterX', 'https://cdn.rawgit.com/photonstorm/phaser/master/filters/BlurX.js');
        //game.load.script('filterY', 'https://cdn.rawgit.com/photonstorm/phaser/master/filters/BlurY.js');
        // load images in preload
        // add expression if content type is image
        angular.forEach(gameContent.elements, function (value, key) {
            game.load.image(value.key, value.content);
        });
        //game.load.image("bg1", '../../asset/bg1.jpg');
        game.load.image("bg2", 'asset/bg2.jpg');
        //game.load.image("bg3", 'asset/bg3.png');
        //game.load.image("bg4", 'asset/bg4.jpg');
    };
    return game;
});
