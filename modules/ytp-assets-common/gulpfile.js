var gulp = require('gulp'),
    runSequence = require('run-sequence'),
    watch = require('gulp-watch'),
    concat = require('gulp-concat'),
    imagemin = require('gulp-imagemin'),
    less = require('gulp-less'),
    prefixer = require('gulp-autoprefixer'),
    clean = require('gulp-clean'),
    template = require('gulp-template'),
    inlineCss = require('gulp-inline-css'),
    base64 = require('gulp-base64');

var paths = {
  src: {
    images: 'src/images/**/*',
    less: 'src/less',
    templates: 'src/templates/**/*',
    static_pages: 'src/static_pages',
    fonts: 'src/fonts/**/*'
  },
  dist: 'resources'
};

var timestamp = new Date().getTime();

gulp.task('clean', function() {
  return gulp.src(paths.dist)
    .pipe(clean());
});

gulp.task('less', function () {
  return gulp.src(paths.src.less+"/*.less")
    .pipe(less({
      paths: [ paths.src.less ]
    }))
    .pipe(prefixer('last 2 versions', 'ie 9'))
    .pipe(template({timestamp: timestamp}))
    .pipe(concat("main.css"))
    .pipe(gulp.dest(paths.dist+'/styles'));
});

gulp.task('images', function() {
  return gulp.src(paths.src.images)
    .pipe(imagemin({optimizationLevel: 5}))
    .pipe(gulp.dest(paths.dist+'/images'));
});

gulp.task('templates', function() {
  return gulp.src(paths.src.templates)
    .pipe(template({timestamp: timestamp}))
    .pipe(gulp.dest(paths.dist+'/templates'));
});


gulp.task('static_css', function(){
    return gulp.src(paths.src.static_pages + "/css/main.css" )
        .pipe(base64())
        .pipe(concat('style.css'))
        .pipe(gulp.dest(paths.src.static_pages + "/css"));
});

gulp.task('static_pages', ['static_css'], function() {
  return gulp.src(paths.src.static_pages + "/*.html")
      .pipe(inlineCss())
      .pipe(gulp.dest(paths.dist + '/static'));
});

gulp.task('fonts', function() {
  return gulp.src(paths.src.fonts)
    .pipe(gulp.dest(paths.dist+'/fonts'));
});

gulp.task('default', function(callback) {
  runSequence('clean',
              ['less', 'templates', 'static_pages', 'images', 'fonts'],
              callback);
});

gulp.task('watch', function () {
  gulp.watch(paths.src.less+'/**/*.less', ['default']);
});