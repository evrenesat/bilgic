angular.module('bilgic')
.factory('Client', function ($http, Settings) {
    var client = {};
    client.getGames = function () {
        return $http.get(Settings.api_url + 'games')
            .success(function (res) {
                return res.data;
            });
    };
    client.getGameLevels = function (key) {
        return $http.get(Settings.api_url + 'game_levels/' + key)
            .success(function (res) {
                return res.data;
            });
    };
    client.getGame = function (key, scope) {
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
    client.saveGames = function () {

    };
    return client;
});