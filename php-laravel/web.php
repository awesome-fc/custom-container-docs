<?php

use Illuminate\Http\Request;
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

Route::get('/', function(Request $request) {
    $requestId = $request -> header('x-fc-request-id');
    return 'Hello FunctionCompute, http function. RequestId: ' . $requestId;
});

Route::post('/invoke', function () {
    return 'Hello FunctionCompute, event function\n';
});
