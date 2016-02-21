angular.module('bilgic')
.factory('Preload', function () {
    var game = {};
    game.preload = function(game, gameContent) {
        game.load.audio('click', 'asset/button_push.mp3');
        game.load.audio('win', 'asset/win.mp3');

        // load images in preload
        // add expression if content type is image
        angular.forEach(gameContent.elements, function (value, key) {
            game.load.image(value.key, 'data:image/jpg;base64,'+value.content);
        });
    };
    return game;
});