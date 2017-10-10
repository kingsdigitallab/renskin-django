// The build will inline common dependencies into this file.
// For any third party dependencies, like jQuery, place them in the lib folder.
// Configure loading modules from the lib directory,
// except for 'app' ones, which are in a sibling
// directory.
requirejs.config({
    baseUrl: '/static/js',
    urlArgs: 'bust=' + (new Date()).getTime(),
    paths: {
        'jquery': '../vendor/jquery/dist/jquery',

        'es6': '../vendor/requirejs-babel/es6',
        'babel': '../vendor/requirejs-babel/babel-5.8.34.min',

        'jscookie': '../vendor/js-cookie/src/js.cookie',

        'requirejs': '../vendor/requirejs/require',
    },
    shim: {
        'jscookie': {
            exports: 'JScookie'
        },
        'ga': {
            exports: '__ga__'
        },
    }
});
