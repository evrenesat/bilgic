angular.module('bilgic')
.factory('Editor', function ($http, Settings) {
    var editor = {};
    editor.search_images = function (kw) {
        return $http.get(Settings.api_url+'search_image/'+kw)
            .success(function (data) {
                return data.results;
            });
    };
    editor.set_level = function (name, elements, game) {
        newElements = [];
        angular.forEach(elements, function (value, key) {
            newElements.push({content: value.content});
        });
        return $http.post(Settings.api_url+'set_level', {level: {name: name, game: game}, elements: newElements });
    };
    return editor;
});