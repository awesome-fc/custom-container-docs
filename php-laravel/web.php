<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/2016-08-15/proxy/CustomContainerDemo/php-laravel-http', function () {
    return 'Hello FunctionCompute, http function\n';
});

Route::post('/invoke', function () {
    return 'Hello FunctionCompute, event function\n';
});
