# -*- coding: utf-8 -*-

from flask import Flask, send_file, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from hashlib import md5

import requests
import base64
import json
import time
import datetime
import os
import traceback
import re

from Configs import *

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@localhost/{}'.format(MYSQL_USER, MYSQL_PASS, MYSQL_DB)
database = SQLAlchemy(app)

details = database.engine.execute("SELECT ID FROM penguins WHERE username = %s", "test")
print 'test', details.first()

PROXIES = []
COLORS = map(str, range(1, 14) + [15, 16])
EMAIL_WELCOME_AUTH_TEXT = '''<html class="gr__localhost"><head> <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <style> *:before {box-sizing: border-box; } *:after {box-sizing: border-box; } body {background: #fff; color: #140b2f; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 16px; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; font-weight: 400; line-height: 28px; overflow-x: hidden; } a:hover {color: #5e35b1; text-decoration: none; } a:focus {color: #5e35b1; text-decoration: none; } a:active {color: #5e35b1; text-decoration: none; } .btn:active {box-shadow: 0 0 0 1px rgba(20, 11, 47, 0.1), 0 0 0 4px rgba(91, 147, 255, 0.25); outline: none; } .btn:focus {box-shadow: 0 0 0 1px rgba(20, 11, 47, 0.1), 0 0 0 4px rgba(91, 147, 255, 0.25); outline: none; } .btn-primary:hover {background-color: #5e35b1; box-shadow: 0 0 0 1px #5e35b1, 0 2px 4px -2px rgba(0, 0, 0, 0.2); color: #fff; } .btn-primary:active {background: #512da8; box-shadow: 0 0 0 1px #512da8, 0 0 0 4px rgba(91, 147, 255, 0.25); color: #fff; } .btn-primary:focus {background: #512da8; box-shadow: 0 0 0 1px #512da8, 0 0 0 4px rgba(91, 147, 255, 0.25); color: #fff; } .btn-secondary:hover {background-color: #fafafb; color: #726d82; } .btn-secondary:focus {background-color: #fafafb; color: #726d82; } .devise-form .help-links a:hover {color: #512da8; } .devise-form .help-links a:focus {color: #512da8; } @keyframes shake {} .form-control:hover {box-shadow: 0 0 0 1px rgba(20, 11, 47, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2); } .form-control:focus {box-shadow: 0 0 0 1px rgba(20, 11, 47, 0.1), 0 0 0 4px rgba(91, 147, 255, 0.25); outline: 0; } .form-control[disabled="disabled"]:hover {border: 1px solid transparent; } .has-error .help-block::first-letter {text-transform: capitalize; } .has-error .form-control:focus {box-shadow: 0 0 0 1px #e45734, 0 2px 4px -2px rgba(0, 0, 0, 0.2); } body {margin: 0; } img {border-style: none; } body {background-color: #fff !important; } @media screen and (max-width: 512px) {.horizontal-form {flex-direction: column; } .horizontal-form .form-control {margin-bottom: 10px; } .flex-group {align-items: stretch; flex-direction: column; } .flex-group.half {max-width: 100%; } .flex-group.quarter {max-width: 100%; } } </style> </head> <body style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); color: #140b2f; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, sans-serif; font-size: 16px; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; font-weight: 400; line-height: 28px; overflow-x: hidden; margin: 0;" bgcolor="#fff" data-gr-c-s-loaded="true"> <div class="dt-container narrow email" style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); max-width: 568px; margin: 0 auto; padding: 48px 24px;"> <div class="hidden" style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); color: #fff; display: none; font-size: 1px; line-height: 1px; max-height: 0; max-width: 0; opacity: 0; overflow: hidden;">Thanks for signing up! You’ve joined an awesome project - Timeline, over 100+ users who love the service we provide.</div> <a href="http://localhost/signup/" style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); color: #512da8; outline: none; text-decoration: none; background-color: transparent; -webkit-text-decoration-skip: objects;" target="_blank">Timeline</a> <p style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); "><img src="https://dovetailapp.com/assets/emails/welcome@2x-0412be5af2894865d654716800bda52958aecd27c5e991ddc7a018b555aff2cf.png" alt="Welcome@2x" style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); display: block; border-radius: 3px; border: none;" width="500" height="308"></p> <h1 id="matthew-welcome-to-dovetail-were-very-excited-youre-here" style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); font-size: 2em; font-weight: 600; line-height: 40px;  padding: 0;">{nickname}, welcome to Timeline! We’re very excited you have joined this amazing project.</h1> <p style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); ">You have successfully registered your penguin, you can anytime login and play the cpps with the username and password you have set</p> <p style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); ">In order to use the nickname as you set in-game, you have to verify this email. Once you do, your nickname is once'n-for-all yours!<br> Click on the button below (or copy paste the link below it in new tab) to authenticate your account. You may (not necessary) want to input your Security Pin during this process.</p> <hr style="box-sizing: content-box; -webkit-tap-highlight-color: rgba(255,255,255,0); background-color: #e7e6ea; height: 1px; overflow: visible; "> <p style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); "><a class="btn btn-primary" href="http://localhost:2083/{username}/auth/{key}" style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); color: #fff; outline: none; text-decoration: none; border-radius: 3px; cursor: pointer; display: inline-block; font-size: 14px; font-weight: 600; height: 40px; text-align: center; -webkit-appearance: none; background-color: #512da8; box-shadow: 0 0 0 1px #512da8,0 2px 4px -2px rgba(0,0,0,0.2); -webkit-text-decoration-skip: objects; padding: 5px 16px; border: 1px solid transparent;" target="_blank">Authenticate This Email</a></p> <p style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); "><a href="http://localhost:2083/{username}/auth/{key}" style="box-sizing: border-box; -webkit-tap-highlight-color: rgba(255,255,255,0); color: #512da8; outline: none; text-decoration: none; background-color: transparent; -webkit-text-decoration-skip: objects;" target="_blank">http://localhost:2083/{username}/auth/{key}</a></p> <hr style="box-sizing: content-box; -webkit-tap-highlight-color: rgba(255,255,255,0); background-color: #e7e6ea; height: 1px; overflow: visible; "> </div>  </body></html>'''
AUTH_PIN_HTML = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="description" content="A front-end template that helps you build fast, modern mobile web apps."><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0"><title>Timeline > Authentication | Valid22.pw</title><meta name="mobile-web-app-capable" content="yes"><link rel="icon" sizes="192x192" href="images/user.jpg"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="Material Design Lite"><link rel="apple-touch-icon-precomposed" href="//localhost/signup/images/ios-desktop.png"><meta name="msapplication-TileImage" content="//localhost/signup/images/user.jpg"><meta name="msapplication-TileColor" content="#3372DF"><link rel="shortcut icon" href="//localhost/signup/images/user.jpg"><link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en"><link rel="stylesheet" href="http://fonts.googleapis.com/icon?family=Material+Icons"><link rel="stylesheet" href="//localhost/signup/css/material.cyan-light_blue.min.css"><link rel="stylesheet" href="//localhost/signup/styles.css"> <script src="//localhost/signup/js/jquery-2.1.4.min.js"></script> <style>#view-source{position:fixed;display:block;right:0;bottom:0;margin-right:40px;margin-bottom:40px;z-index:900}</style><!-- Global site tag (gtag.js) - Google Analytics --> <script async src="http://www.googletagmanager.com/gtag/js?id=UA-57990863-2"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'UA-57990863-2'); </script> </head><body><div class="demo-layout mdl-layout mdl-js-layout mdl-layout--fixed-drawer mdl-layout--fixed-header"> <header class="demo-header mdl-layout__header mdl-color--grey-100 mdl-color-text--grey-600"><div class="mdl-layout__header-row"> <span class="mdl-layout-title">Timeline - Auth</span><div class="mdl-layout-spacer"></div><div class="mdl-textfield mdl-js-textfield mdl-textfield--expandable"> <label class="mdl-button mdl-js-button mdl-button--icon" for="search"> <i class="material-icons">search</i> </label><div class="mdl-textfield__expandable-holder"> <input class="mdl-textfield__input" type="text" id="search"> <label class="mdl-textfield__label" for="search">Enter your query...</label></div></div> <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="hdrbtn"> <i class="material-icons">more_vert</i> </button><ul class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="hdrbtn"><li class="mdl-menu__item">About</li><li class="mdl-menu__item">Contact</li></ul><div class="mdl-tooltip mdl-tooltip--large" for="hdrbtn"> Quick Help</div></div> </header><div class="demo-drawer mdl-layout__drawer mdl-color--blue-grey-900 mdl-color-text--blue-grey-50"> <header class="demo-drawer-header"> <img src="//localhost/signup/images/user.jpg" class="demo-avatar"><div class="demo-avatar-dropdown"> <span>${USERNAME}$, Welcome</span><div class="mdl-layout-spacer"></div> <button id="accbtn" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon"> <i class="material-icons" role="presentation">arrow_drop_down</i> <span class="visuallyhidden">Accounts</span> </button><ul class="mdl-menu mdl-menu--bottom-right mdl-js-menu mdl-js-ripple-effect" for="accbtn"><li class="mdl-menu__item"><i class="material-icons">add</i>Accounts (coming soon)</li></ul><div class="mdl-tooltip mdl-tooltip--large" for="accbtn"> Account Manager</div></div> </header> <nav class="demo-navigation mdl-navigation mdl-color--blue-grey-800"> <a class="mdl-navigation__link" href="index.html"><i class="mdl-color-text--blue-grey-400 material-icons" role="presentation">home</i>Home</a> </nav></div> <main class="mdl-layout__content mdl-color--grey-100"><div class="mdl-grid demo-content"><div id="authcdn" class="mdl-grid demo-content mdl-cell mdl-cell--12-col mdl-cell--12-col-desktop"><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop"><div class="mdl-card mdl-shadow--6dp"><div class="mdl-card__title mdl-color--primary mdl-color-text--white" style="background:rgb(255, 152, 0) !important;"><h2 class="mdl-card__title-text">Authenticate Your Account</h2></div><div class="mdl-card__supporting-text"><form action="#"><div class="mdl-textfield mdl-js-textfield"> <input class="mdl-textfield__input" type="text" id="username" disabled="" value="${USERNAME}$" /> <label class="mdl-textfield__label" for="username">Username</label></div><div class="mdl-textfield mdl-js-textfield"> <input class="mdl-textfield__input" type="password" id="userkey" disabled="" value="${AUTH_KEY}$" /> <label class="mdl-textfield__label" for="userkey">Authentication Key</label></div><div class="mdl-textfield mdl-js-textfield"> <input class="mdl-textfield__input" type="number" disabled="" value="2222" id="userpin" autofocus="autofocus" max="9999" min="1000" /> <label class="mdl-textfield__label" for="userpin">Security Pin</label></div><a href="javascript:0;" id="authclick" class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white" style="background: rgb(139, 195, 74);">Click here to authenticate</a></form></div></div></div></div><div id="success" style="display: none;"><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop"><div class="mdl-card mdl-shadow--6dp"><div class="mdl-card__title mdl-color--primary mdl-color-text--white" style="background: rgb(76, 175, 80) !important;"><h2 class="mdl-card__title-text">Successfully Authenticated!</h2></div><div class="mdl-card__supporting-text"><p id="success-text">Your account has been verified successfully!</p> <br> <a href="//localhost/signup/play.html" id="signupsubmit" class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white">Play now</a></div></div></div></div><div id="error" style="display: none;"><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop"><div class="mdl-card mdl-shadow--6dp"><div class="mdl-card__title mdl-color--primary mdl-color-text--white" style="background: rgb(244, 67, 54) !important;"><h2 class="mdl-card__title-text">Authentication Failed!</h2></div><div class="mdl-card__supporting-text"><p id="success-text">Unable to authenticate your account, try again or contact support!</p></div></div></div></div><div class="mdl-cell mdl-cell--12-col "><div class="mdl-card mdl-shadow--6dp mdl-cell mdl-cell--12-col"><div class="mdl-card__title mdl-color--primary mdl-color-text--white"><h2 class="mdl-card__title-text">Advertisement</h2></div><div class="mdl-card__supporting-text"> <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script> <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-4551959209089511" data-ad-slot="1633147462" data-ad-format="auto"></ins> <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script> </div></div></div></div> </main><center style="z-index:10;"><div><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop" style="z-index: 10; display: none;" id="ovloader"><div id="p2loader" class="mdl-progress mdl-js-progress mdl-progress__indeterminate is-upgraded" data-upgraded=",MaterialProgress"><div class="progressbar bar bar1" style="width: 0%;"></div><div class="bufferbar bar bar2" style="width: 100%;"></div><div class="auxbar bar bar3" style="width: 0%;"></div></div></div></div></center><div id="overlay-loader" class="mdl-layout__obfuscator is-visible" style="display: none;"></div></div> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <mask id="piemask" maskContentUnits="objectBoundingBox"> <circle cx=0.5 cy=0.5 r=0.49 fill="white" /> <circle cx=0.5 cy=0.5 r=0.40 fill="black" /> </mask> <g id="piechart"> <circle cx=0.5 cy=0.5 r=0.5 /> <path d="M 0.5 0.5 0.5 0 A 0.5 0.5 0 0 1 0.95 0.28 z" stroke="none" fill="rgba(255, 255, 255, 0.75)" /> </g> </defs> </svg> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <mask id="piemask2" maskContentUnits="objectBoundingBox"> <circle cx=0.5 cy=0.5 r=0.49 fill="white" /> <circle cx=0.5 cy=0.5 r=0.40 fill="black" /> </mask> <g id="piechart2"> <circle cx=0.5 cy=0.5 r=0.5 /> <path d="M 0.5 0.5 0.5 0 A 0.5 0.5 0 0 1 0.95 0.28 z" stroke="none" fill="rgba(255, 255, 255, 0.75)" /> </g> </defs> </svg> <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 500 250" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <g id="chart"> <g id="Gridlines"> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="27.3" x2="468.3" y2="27.3" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="66.7" x2="468.3" y2="66.7" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="105.3" x2="468.3" y2="105.3" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="144.7" x2="468.3" y2="144.7" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="184.3" x2="468.3" y2="184.3" /> </g> <g id="Numbers"> <text transform="matrix(1 0 0 1 485 29.3333)" fill="#888888" font-family="'Roboto'" font-size="9">500</text> <text transform="matrix(1 0 0 1 485 69)" fill="#888888" font-family="'Roboto'" font-size="9">400</text> <text transform="matrix(1 0 0 1 485 109.3333)" fill="#888888" font-family="'Roboto'" font-size="9">300</text> <text transform="matrix(1 0 0 1 485 149)" fill="#888888" font-family="'Roboto'" font-size="9">200</text> <text transform="matrix(1 0 0 1 485 188.3333)" fill="#888888" font-family="'Roboto'" font-size="9">100</text> <text transform="matrix(1 0 0 1 0 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">1</text> <text transform="matrix(1 0 0 1 78 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">2</text> <text transform="matrix(1 0 0 1 154.6667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">3</text> <text transform="matrix(1 0 0 1 232.1667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">4</text> <text transform="matrix(1 0 0 1 309 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">5</text> <text transform="matrix(1 0 0 1 386.6667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">6</text> <text transform="matrix(1 0 0 1 464.3333 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">7</text> </g> <g id="Layer_5"> <polygon opacity="0.36" stroke-miterlimit="10" points="0,223.3 48,138.5 154.7,169 211,88.5 294.5,80.5 380,165.2 437,75.5 469.5,223.3 	"/> </g> <g id="Layer_4"> <polygon stroke-miterlimit="10" points="469.3,222.7 1,222.7 48.7,166.7 155.7,188.3 212,132.7 296.7,128 380.7,184.3 436.7,125 	"/> </g> </g> </defs> </svg> <script src="//localhost/signup/js/material.min.js"></script> <script src="//localhost/signup/js/auth.js"></script> </body></html>'''
AUTH_USER_NOT_EXISTS = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="description" content="A front-end template that helps you build fast, modern mobile web apps."><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0"><title>Timeline > Authentication | Valid22.pw</title><meta name="mobile-web-app-capable" content="yes"><link rel="icon" sizes="192x192" href="//localhost/signup/images/user.jpg"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="Material Design Lite"><link rel="apple-touch-icon-precomposed" href="//localhost/signup/images/ios-desktop.png"><meta name="msapplication-TileImage" content="//localhost/signup/images/user.jpg"><meta name="msapplication-TileColor" content="#3372DF"><link rel="shortcut icon" href="images/user.jpg"><link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en"><link rel="stylesheet" href="http://fonts.googleapis.com/icon?family=Material+Icons"><link rel="stylesheet" href="//localhost/signup/css/material.cyan-light_blue.min.css"><link rel="stylesheet" href="//localhost/signup/styles.css"> <script src="//localhost/signup/js/jquery-2.1.4.min.js"></script> <style>#view-source{position:fixed;display:block;right:0;bottom:0;margin-right:40px;margin-bottom:40px;z-index:900}</style><!-- Global site tag (gtag.js) - Google Analytics --> <script async src="http://www.googletagmanager.com/gtag/js?id=UA-57990863-2"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'UA-57990863-2'); </script> </head><body><div class="demo-layout mdl-layout mdl-js-layout mdl-layout--fixed-drawer mdl-layout--fixed-header"> <header class="demo-header mdl-layout__header mdl-color--grey-100 mdl-color-text--grey-600"><div class="mdl-layout__header-row"> <span class="mdl-layout-title">Timeline - Auth</span><div class="mdl-layout-spacer"></div><div class="mdl-textfield mdl-js-textfield mdl-textfield--expandable"> <label class="mdl-button mdl-js-button mdl-button--icon" for="search"> <i class="material-icons">search</i> </label><div class="mdl-textfield__expandable-holder"> <input class="mdl-textfield__input" type="text" id="search"> <label class="mdl-textfield__label" for="search">Enter your query...</label></div></div> <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="hdrbtn"> <i class="material-icons">more_vert</i> </button><ul class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="hdrbtn"><li class="mdl-menu__item">About</li><li class="mdl-menu__item">Contact</li></ul><div class="mdl-tooltip mdl-tooltip--large" for="hdrbtn"> Quick Help</div></div> </header><div class="demo-drawer mdl-layout__drawer mdl-color--blue-grey-900 mdl-color-text--blue-grey-50"> <header class="demo-drawer-header"> <img src="//localhost/signup/images/user.jpg" class="demo-avatar"><div class="demo-avatar-dropdown"> <span>Guest, Welcome</span><div class="mdl-layout-spacer"></div> <button id="accbtn" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon"> <i class="material-icons" role="presentation">arrow_drop_down</i> <span class="visuallyhidden">Accounts</span> </button><ul class="mdl-menu mdl-menu--bottom-right mdl-js-menu mdl-js-ripple-effect" for="accbtn"><li class="mdl-menu__item"><i class="material-icons">add</i>Accounts (coming soon)</li></ul><div class="mdl-tooltip mdl-tooltip--large" for="accbtn"> Account Manager</div></div> </header> <nav class="demo-navigation mdl-navigation mdl-color--blue-grey-800"> <a class="mdl-navigation__link" href="index.html"><i class="mdl-color-text--blue-grey-400 material-icons" role="presentation">home</i>Home</a> </nav></div> <main class="mdl-layout__content mdl-color--grey-100"><div class="mdl-grid demo-content"><div id="error" style="display: block;"><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop"><div class="mdl-card mdl-shadow--6dp"><div class="mdl-card__title mdl-color--primary mdl-color-text--white" style="background: rgb(244, 67, 54) !important;"><h2 class="mdl-card__title-text">Authentication Failed!</h2></div><div class="mdl-card__supporting-text"><p id="success-text">An error occured while authenticating your account. Either Username doesn't exists or user and key doesn't match! Please try again or contact support.</p></div></div></div></div><div class="mdl-cell mdl-cell--12-col "><div class="mdl-card mdl-shadow--6dp mdl-cell mdl-cell--12-col"><div class="mdl-card__title mdl-color--primary mdl-color-text--white"><h2 class="mdl-card__title-text">Advertisement</h2></div><div class="mdl-card__supporting-text"> <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script> <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-4551959209089511" data-ad-slot="1633147462" data-ad-format="auto"></ins> <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script> </div></div></div></div> </main><center style="z-index:10;"><div><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop" style="z-index: 10; display: none;" id="ovloader"><div id="p2loader" class="mdl-progress mdl-js-progress mdl-progress__indeterminate is-upgraded" data-upgraded=",MaterialProgress"><div class="progressbar bar bar1" style="width: 0%;"></div><div class="bufferbar bar bar2" style="width: 100%;"></div><div class="auxbar bar bar3" style="width: 0%;"></div></div></div></div></center><div id="overlay-loader" class="mdl-layout__obfuscator is-visible" style="display: none;"></div></div> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <mask id="piemask" maskContentUnits="objectBoundingBox"> <circle cx=0.5 cy=0.5 r=0.49 fill="white" /> <circle cx=0.5 cy=0.5 r=0.40 fill="black" /> </mask> <g id="piechart"> <circle cx=0.5 cy=0.5 r=0.5 /> <path d="M 0.5 0.5 0.5 0 A 0.5 0.5 0 0 1 0.95 0.28 z" stroke="none" fill="rgba(255, 255, 255, 0.75)" /> </g> </defs> </svg> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <mask id="piemask2" maskContentUnits="objectBoundingBox"> <circle cx=0.5 cy=0.5 r=0.49 fill="white" /> <circle cx=0.5 cy=0.5 r=0.40 fill="black" /> </mask> <g id="piechart2"> <circle cx=0.5 cy=0.5 r=0.5 /> <path d="M 0.5 0.5 0.5 0 A 0.5 0.5 0 0 1 0.95 0.28 z" stroke="none" fill="rgba(255, 255, 255, 0.75)" /> </g> </defs> </svg> <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 500 250" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <g id="chart"> <g id="Gridlines"> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="27.3" x2="468.3" y2="27.3" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="66.7" x2="468.3" y2="66.7" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="105.3" x2="468.3" y2="105.3" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="144.7" x2="468.3" y2="144.7" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="184.3" x2="468.3" y2="184.3" /> </g> <g id="Numbers"> <text transform="matrix(1 0 0 1 485 29.3333)" fill="#888888" font-family="'Roboto'" font-size="9">500</text> <text transform="matrix(1 0 0 1 485 69)" fill="#888888" font-family="'Roboto'" font-size="9">400</text> <text transform="matrix(1 0 0 1 485 109.3333)" fill="#888888" font-family="'Roboto'" font-size="9">300</text> <text transform="matrix(1 0 0 1 485 149)" fill="#888888" font-family="'Roboto'" font-size="9">200</text> <text transform="matrix(1 0 0 1 485 188.3333)" fill="#888888" font-family="'Roboto'" font-size="9">100</text> <text transform="matrix(1 0 0 1 0 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">1</text> <text transform="matrix(1 0 0 1 78 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">2</text> <text transform="matrix(1 0 0 1 154.6667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">3</text> <text transform="matrix(1 0 0 1 232.1667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">4</text> <text transform="matrix(1 0 0 1 309 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">5</text> <text transform="matrix(1 0 0 1 386.6667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">6</text> <text transform="matrix(1 0 0 1 464.3333 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">7</text> </g> <g id="Layer_5"> <polygon opacity="0.36" stroke-miterlimit="10" points="0,223.3 48,138.5 154.7,169 211,88.5 294.5,80.5 380,165.2 437,75.5 469.5,223.3 	"/> </g> <g id="Layer_4"> <polygon stroke-miterlimit="10" points="469.3,222.7 1,222.7 48.7,166.7 155.7,188.3 212,132.7 296.7,128 380.7,184.3 436.7,125 	"/> </g> </g> </defs> </svg> <script src="//localhost/signup/js/material.min.js"></script> </body></html>'''
AUTH_ALREADY_DONE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="description" content="A front-end template that helps you build fast, modern mobile web apps."><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0"><title>Timeline > Authentication | Valid22.pw</title><meta name="mobile-web-app-capable" content="yes"><link rel="icon" sizes="192x192" href="//localhost/signup/images/user.jpg"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="Material Design Lite"><link rel="apple-touch-icon-precomposed" href="//localhost/signup/images/ios-desktop.png"><meta name="msapplication-TileImage" content="//localhost/signup/images/user.jpg"><meta name="msapplication-TileColor" content="#3372DF"><link rel="shortcut icon" href="images/user.jpg"><link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en"><link rel="stylesheet" href="http://fonts.googleapis.com/icon?family=Material+Icons"><link rel="stylesheet" href="//localhost/signup/css/material.cyan-light_blue.min.css"><link rel="stylesheet" href="//localhost/signup/styles.css"> <script src="//localhost/signup/js/jquery-2.1.4.min.js"></script> <style>#view-source{position:fixed;display:block;right:0;bottom:0;margin-right:40px;margin-bottom:40px;z-index:900}</style><!-- Global site tag (gtag.js) - Google Analytics --> <script async src="http://www.googletagmanager.com/gtag/js?id=UA-57990863-2"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'UA-57990863-2'); </script> </head><body><div class="demo-layout mdl-layout mdl-js-layout mdl-layout--fixed-drawer mdl-layout--fixed-header"> <header class="demo-header mdl-layout__header mdl-color--grey-100 mdl-color-text--grey-600"><div class="mdl-layout__header-row"> <span class="mdl-layout-title">Timeline - Auth</span><div class="mdl-layout-spacer"></div><div class="mdl-textfield mdl-js-textfield mdl-textfield--expandable"> <label class="mdl-button mdl-js-button mdl-button--icon" for="search"> <i class="material-icons">search</i> </label><div class="mdl-textfield__expandable-holder"> <input class="mdl-textfield__input" type="text" id="search"> <label class="mdl-textfield__label" for="search">Enter your query...</label></div></div> <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="hdrbtn"> <i class="material-icons">more_vert</i> </button><ul class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="hdrbtn"><li class="mdl-menu__item">About</li><li class="mdl-menu__item">Contact</li></ul><div class="mdl-tooltip mdl-tooltip--large" for="hdrbtn"> Quick Help</div></div> </header><div class="demo-drawer mdl-layout__drawer mdl-color--blue-grey-900 mdl-color-text--blue-grey-50"> <header class="demo-drawer-header"> <img src="//localhost/signup/images/user.jpg" class="demo-avatar"><div class="demo-avatar-dropdown"> <span>Guest, Welcome</span><div class="mdl-layout-spacer"></div> <button id="accbtn" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon"> <i class="material-icons" role="presentation">arrow_drop_down</i> <span class="visuallyhidden">Accounts</span> </button><ul class="mdl-menu mdl-menu--bottom-right mdl-js-menu mdl-js-ripple-effect" for="accbtn"><li class="mdl-menu__item"><i class="material-icons">add</i>Accounts (coming soon)</li></ul><div class="mdl-tooltip mdl-tooltip--large" for="accbtn"> Account Manager</div></div> </header> <nav class="demo-navigation mdl-navigation mdl-color--blue-grey-800"> <a class="mdl-navigation__link" href="index.html"><i class="mdl-color-text--blue-grey-400 material-icons" role="presentation">home</i>Home</a> </nav></div> <main class="mdl-layout__content mdl-color--grey-100"><div class="mdl-grid demo-content"><div id="error" style="display: block;"><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop"><div class="mdl-card mdl-shadow--6dp"><div class="mdl-card__title mdl-color--primary mdl-color-text--white" style="background: rgb(76, 175, 80) !important;"><h2 class="mdl-card__title-text">o_OPs!</h2></div><div class="mdl-card__supporting-text"><p id="success-text">This account is already authenticated!</p></div></div></div></div><div class="mdl-cell mdl-cell--12-col "><div class="mdl-card mdl-shadow--6dp mdl-cell mdl-cell--12-col"><div class="mdl-card__title mdl-color--primary mdl-color-text--white"><h2 class="mdl-card__title-text">Advertisement</h2></div><div class="mdl-card__supporting-text"> <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script> <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-4551959209089511" data-ad-slot="1633147462" data-ad-format="auto"></ins> <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script> </div></div></div></div> </main><center style="z-index:10;"><div><div class="mdl-cell mdl-cell--4-col mdl-cell--4-col-desktop" style="z-index: 10; display: none;" id="ovloader"><div id="p2loader" class="mdl-progress mdl-js-progress mdl-progress__indeterminate is-upgraded" data-upgraded=",MaterialProgress"><div class="progressbar bar bar1" style="width: 0%;"></div><div class="bufferbar bar bar2" style="width: 100%;"></div><div class="auxbar bar bar3" style="width: 0%;"></div></div></div></div></center><div id="overlay-loader" class="mdl-layout__obfuscator is-visible" style="display: none;"></div></div> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <mask id="piemask" maskContentUnits="objectBoundingBox"> <circle cx=0.5 cy=0.5 r=0.49 fill="white" /> <circle cx=0.5 cy=0.5 r=0.40 fill="black" /> </mask> <g id="piechart"> <circle cx=0.5 cy=0.5 r=0.5 /> <path d="M 0.5 0.5 0.5 0 A 0.5 0.5 0 0 1 0.95 0.28 z" stroke="none" fill="rgba(255, 255, 255, 0.75)" /> </g> </defs> </svg> <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <mask id="piemask2" maskContentUnits="objectBoundingBox"> <circle cx=0.5 cy=0.5 r=0.49 fill="white" /> <circle cx=0.5 cy=0.5 r=0.40 fill="black" /> </mask> <g id="piechart2"> <circle cx=0.5 cy=0.5 r=0.5 /> <path d="M 0.5 0.5 0.5 0 A 0.5 0.5 0 0 1 0.95 0.28 z" stroke="none" fill="rgba(255, 255, 255, 0.75)" /> </g> </defs> </svg> <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 500 250" style="position: fixed; left: -1000px; height: -1000px;"> <defs> <g id="chart"> <g id="Gridlines"> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="27.3" x2="468.3" y2="27.3" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="66.7" x2="468.3" y2="66.7" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="105.3" x2="468.3" y2="105.3" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="144.7" x2="468.3" y2="144.7" /> <line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="184.3" x2="468.3" y2="184.3" /> </g> <g id="Numbers"> <text transform="matrix(1 0 0 1 485 29.3333)" fill="#888888" font-family="'Roboto'" font-size="9">500</text> <text transform="matrix(1 0 0 1 485 69)" fill="#888888" font-family="'Roboto'" font-size="9">400</text> <text transform="matrix(1 0 0 1 485 109.3333)" fill="#888888" font-family="'Roboto'" font-size="9">300</text> <text transform="matrix(1 0 0 1 485 149)" fill="#888888" font-family="'Roboto'" font-size="9">200</text> <text transform="matrix(1 0 0 1 485 188.3333)" fill="#888888" font-family="'Roboto'" font-size="9">100</text> <text transform="matrix(1 0 0 1 0 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">1</text> <text transform="matrix(1 0 0 1 78 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">2</text> <text transform="matrix(1 0 0 1 154.6667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">3</text> <text transform="matrix(1 0 0 1 232.1667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">4</text> <text transform="matrix(1 0 0 1 309 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">5</text> <text transform="matrix(1 0 0 1 386.6667 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">6</text> <text transform="matrix(1 0 0 1 464.3333 249.0003)" fill="#888888" font-family="'Roboto'" font-size="9">7</text> </g> <g id="Layer_5"> <polygon opacity="0.36" stroke-miterlimit="10" points="0,223.3 48,138.5 154.7,169 211,88.5 294.5,80.5 380,165.2 437,75.5 469.5,223.3 	"/> </g> <g id="Layer_4"> <polygon stroke-miterlimit="10" points="469.3,222.7 1,222.7 48.7,166.7 155.7,188.3 212,132.7 296.7,128 380.7,184.3 436.7,125 	"/> </g> </g> </defs> </svg> <script src="//localhost/signup/js/material.min.js"></script> </body></html>'''

def sendEmail(username, user_email, msg):
	if EMAIL_SMTP_USERNAME is None or EMAIL_SMTP_SERVER_NAME is None:
		return

	import smtplib
	import email.utils
	from email.mime.text import MIMEText

	# Prompt the user for connection info
	servername = EMAIL_SMTP_SERVER_NAME
	username = EMAIL_SMTP_USERNAME
	password = EMAIL_SMTP_PASSWORD

	# Create the message
	msg = MIMEText(msg, 'html')
	msg.set_unixfrom('Support : Timeline')
	msg['To'] = email.utils.formataddr((username, user_email))
	msg['From'] = email.utils.formataddr(('Support : Timeline', 'support@timeline'))
	msg['Subject'] = 'Timeline Account - Email Authentication'

	server = smtplib.SMTP(servername)
	try:
		server.set_debuglevel(False)

		# identify ourselves, prompting server for supported features
		server.ehlo()

		# If we can encrypt this session, do it
		if server.has_extn('STARTTLS'):
			server.starttls()
			server.ehlo() # re-identify ourselves over TLS connection

		server.login(username, password)
		msg = msg.as_string()
		server.sendmail('support@timeline', [user_email], msg)
	except:
		pass
	finally:
		server.quit()

def sendWelcomeAuth(username, nickname, key, email):
	msg = EMAIL_WELCOME_AUTH_TEXT.replace('{nickname}', nickname).replace('{username}', username).replace('{key}', key)
	sendEmail(username, email, msg)

def generateProxy():
	url = 'https://gimmeproxy.com/api/getProxy?get=true&protocol=http&supportsHttps=true'
	proxy = requests.get(url)

	data = json.loads(proxy.text)
	PROXIES.append([data, 0, time.time()])

def getProxy():
	availableProxies = []
	now = time.time()
	for i in range(len(PROXIES)):
		p = PROXIES[i]
		proxy, count, last_used = p

		if (count > 9 and ((now - last_used)/60/60) < 1) or (((now - last_used)/60/60) > 1):
			generateProxy()
			PROXIES[i] = PROXIES[-1]
			del PROXIES[-1]
			continue

		PROXIES[i] = [proxy, count, last_used]
		availableProxies.append(i)

	if len(availableProxies) < 1:
		generateProxy()
		return getProxy()

	return availableProxies[0]

def isValidEmail(email):
	return re.match(r'[^@]+@[^@]+\.[^@]+', email)

def emailHealthCheck(email):
	if not isValidEmail(email):
		return [False, 'Invalid Email Address.']

	url = 'http://api.antideo.com/email/{}'.format(email)

	proxyId = getProxy()
	PROXIES[proxyId][1] += 1
	proxy = PROXIES[proxyId][0]

	proxyType = proxy['type']
	ipPort = proxy['ipPort']
	proxies = {proxyType : "{}://{}".format(proxyType, ipPort)}

	session = requests.Session()
	session.proxies = proxies

	check = session.get(url)

	healthResponse = json.loads(check.text)
	if 'error' in healthResponse:
		return [False, 'Invalid Email Address.']

	if healthResponse['spam'] or healthResponse['scam']:
		return [False, 'Email address entered is found to be a spam or scam.']

	if healthResponse['disposable']:
		return [False, 'Email address you entered is disposable, use a legit email address.']

	url = 'https://apilayer.net/api/check?access_key={}&email={}'.format(API_LAYER_KEY, email)
	check = session.get(url)
	
	existsCheck = json.loads(check.text)

	if 'error' in existsCheck:
		return [True, '']

	if not existsCheck['smtp_check']:
		return [False, "Email doesn't exist. Use a real email address."]

	return [True, '']

def checkRecaptcha(resp):
	url = "https://www.google.com/recaptcha/api/siteverify"
	secret = RECAPTCHA_SECRET

	botCheck = requests.post(url, data = {"secret" : secret, "response" : resp})
	response = json.loads(botCheck.text)

	return response['success']

def encodePin(pin):
	pinb64 = base64.b64encode(pin)
	pin64 = pinb64[3:] + pinb64[:3]

	pinEncoded = base64.b64encode(pinb64)
	return md5(pinEncoded).hexdigest()

def encodePassword(password):
	pinb64 = base64.b64encode(password)
	pin64 = pinb64[22:] + pinb64[:22]

	pinEncoded = base64.b64encode(pinb64)
	return md5(pinEncoded).hexdigest()

@app.route("/register/<data>", methods = ['POST'])
def signup(data):
	print 'yep?', data
	error_list = list()

	try:
		if not request.form.has_key('recaptcha'):
			return abort(404)

		if not checkRecaptcha(request.form.get('recaptcha')):
			print 'recaptcha oopies'
			return abort(404)

		details = base64.b64decode(data).split(';')
		username, password, email, userpin, nickname, color, member, toc = map(lambda x: base64.b64decode(x).strip(' '), details)
		userpin = '2222'
		member = int(member) if member.isdigit() else 1

		if not username.replace(' ', '').isalnum():
			error_list.append({'title': 'Username', 'ref': 'username', 'msg':'Username may contain only alphabets, numbers and spaces.'})

		if not nickname.replace(' ', '').isalnum():
			error_list.append({'title': 'Nickname', 'ref': 'usernick', 'msg':'Nickname may contain only alphabets, numbers and spaces.'})

		if len(username) < 4 or len(username) > 12:
			error_list.append({'title': 'Username', 'ref': 'username', 'msg':'Username must contain a minimum of 4 characters and a maximum of 12.'})

		if len(nickname) < 4 or len(nickname) > 12:
			error_list.append({'title': 'Nickname', 'ref': 'usernick', 'msg':'Nickname must contain a minimum of 4 characters and a maximum of 12.'})

		try:
			email_check, error_mag = emailHealthCheck(email)
			if not email_check:
				error_list.append({'title': 'Email', 'ref': 'useremail', 'msg': error_mag})
		except:
			pass

		if not str(userpin).isdigit() or len(str(userpin)) != 4:
			error_list.append({'title': 'Secret Pin', 'ref': 'userpin', 'msg':'Security Pin should be a 4 digit number.'})

		if not 5 <= len(password) <= 20:
			error_list.append({'title': 'Password', 'ref': 'userpass', 'msg':'Password should be a minimum of 4 characters and a maximum of 20.'})

		if not color in COLORS:
			error_list.append({'title': 'Color', 'ref': 'usercolor', 'msg':'Please choose a valid color.'})

		if not toc.isdigit() or not int(toc):
			error_list.append({'title': 'Terms and Policy', 'ref': 'userterms', 'msg':'You must agree to the Terms and Policy before signup.'})

		if len(error_list) > 0:
			return jsonify(success = False, error = error_list)

		engine = database.engine.connect()

		details = engine.execute("SELECT ID FROM penguins WHERE username = %s", username)
		details = details.first()

		if details is not None:
			error_list.append({'title': 'Username', 'ref': 'username', 'msg':'Username already exists, try another one.'})

		details = engine.execute("SELECT ID FROM penguins WHERE email = %s", email)
		details = details.first()
		if details is not None:
			error_list.append({'title': 'Email', 'ref': 'useremail', 'msg': "That email is already registered to another penguin, try another one."})

		if len(error_list) > 0:
			return jsonify(success = False, error = error_list)

		membership = '{} 00:00:00'.format((datetime.date.today() + datetime.timedelta(member * 6*365/12)).isoformat())
		password = md5(password).hexdigest()
		userpin = encodePin(userpin)
		signup = engine.execute("INSERT INTO `penguins` (`username`, `password`, `nickname`, `email`, `coins`, `igloos`, `furnitures`, `floors`, `locations`, `care`, `stamps`, `cover`, `color`, `membership`, `inventory`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
			username, password, username, email, 5000, '', '', '', '', '', '', '', color, membership, '{}%1600'.format(color)
		)

		penguin_id = signup.lastrowid
		authKey = os.urandom(24).encode('hex')
		engine.execute("UPDATE `penguins` SET `hash` = %s, `Nickname` = %s WHERE `ID` = %s", '{};{}'.format(authKey, nickname), 'P{}'.format(penguin_id), penguin_id)

		sendWelcomeAuth(username, nickname, authKey, email)

	except Exception, e:
		print e
		traceback.print_exc()
		return abort(404)

	is_success = len(error_list) < 1
	return jsonify(success = is_success, error = error_list)


@app.route("/<user>/auth/<key>", methods = ['GET'])
def handleInitAuth(user, key):
	try:
		authHtml = AUTH_PIN_HTML.replace('${USERNAME}$', user).replace('${AUTH_KEY}$', key)

		engine = database.engine.connect()

		details = engine.execute("SELECT hash FROM penguins WHERE username = %s", user)
		details = details.first()
		if details is None:
			authHtml = AUTH_USER_NOT_EXISTS

		else:
			detail = details[0]

			if detail is None or detail == '':
				authHtml = AUTH_ALREADY_DONE
			else:
				authKey, nickname = detail.split(';')
				if authKey != key:
					authHtml = AUTH_USER_NOT_EXISTS

		return Response(authHtml, mimetype='text/html')
	except:
		traceback.print_exc()
		return abort(404)

@app.route("/auth/<authKey>", methods = ['POST'])
def handleDoAuth(authKey):
	try:
		keyList = base64.b64decode(authKey).split(';')
		user, key = map(base64.b64decode, keyList)
		pin = base64.b64decode(request.form.get('pin'))

		engine = database.engine.connect()

		details = engine.execute("SELECT hash FROM penguins WHERE username = %s", user)
		details = details.first()
		if details is None:
			return jsonify(success = False)

		if pin != '2222':
			return jsonify(success = False)

		detail = details[0]
		akey, nickname = detail.split(';')
		if akey != key:
			return jsonify(success = False)

		engine.execute("UPDATE penguins SET hash = NULL, nickname = %s WHERE username = %s", nickname, user)

	except:
		traceback.print_exc()
		return jsonify(success = False)

	return jsonify(success = True)

#app.run(host = 'localhost', port = 2083, threaded = True, debug=True, ssl_context = ('/path/to/credentials.pem', '/path/to/credentials.key'))
app.run(host = 'localhost', port = 2083, threaded = True, debug=True)