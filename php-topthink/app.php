<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006~2018 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: liu21st <liu21st@gmail.com>
// +----------------------------------------------------------------------
use think\facade\Route;
use think\facade\Request;

Route::post('invoke', function () {
    $headerInfo = Request::header();
    return 'Hello from Function Compute event trigger. Request\'s full header array is: '.json_encode($headerInfo);
});

Route::post('initialize', function () {
    return 'Hello from Function Compute! Function initialized.';
});

Route::get('/', function () {
    return 'Hello from Function Compute HTTP GET Trigger.';
});

Route::post('header/:header', function () {
    echo 'Hello from Function Compute HTTP trigger. ';
    $headerKey = Request::param('header');
    $headerInfo = Request::header();
    if (array_key_exists($headerKey, $headerInfo)) {
        return 'Header \''.$headerKey.'\' is: '.$headerInfo[$headerKey];
    }
    return 'No such header exists';
});

Route::post('/', function () {
    return 'Hello from Function Compute HTTP POST Trigger.';
});
