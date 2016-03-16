/**
 * Created by justus on 13/03/16.
 */

var app = angular.module('product', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}])

app.controller('TestCtrl', function(){
    this.testProduct = 'something should go here';
});

app.controller('CountCtrl', function($scope){
   $scope.count = 0;
});