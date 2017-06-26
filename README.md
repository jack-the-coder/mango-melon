# Project Mango Melon (v3, codenamed Operation King Tut)

Operation King Tut is the third version of the existing Project Mango Melon. You can check it out at mango-melon-p4200.herokuapp.com.

Project Mango Melon is backend (and some half-completed JavaScript front-end) code for a social network. It is generally easy to customize. Other projects can be easily based on this one by simply forking it and modifying the code. 

Its development has now stopped, because I (the developer) chose to work on other projects that were more important (and may or may not incorporate code from PMM). However, the code is mostly complete. 

## SECURITY ADVISORY: 

**PLEASE** verify that this code is secure before deploying it to any production environment. Although I *think* that the password hashing function (`bcrypt`) is secure and implemented correctly, I am not a security expert and none of the code has been verified. 

Use this code at your own risk if you should choose to incorporate it into a production application. 

## Changes from PMM Classic:

- Use Framework7 for front-end.
- Use same Flask based middle-end with Jinja2 template engine and Peewee database engine, but with quite a bit of modified code.
- May change hosting provider to AWS or to Azure, in which case I will use a different database software. However, this is not likely. I will probably use Heroku as I have.
- Single-page front end layout with various forms on one page.
- Lazy loader in JS from F7.
- Support for native APIs when transitioning to a Progressive Web App.
- Support for Apache Cordova and Adobe PhoneGap.
- POSSIBLE: Support for Electron.
- POSSIBLE: Desktop notifications integrations.
- POSSIBLE: Change to multi page layout on desktop.

## News:

Recently, the project got a completely new direction, and so it made sense to separate the development of Project Mango Melon v2 and v3, as this involved a big change. 

This repository will also change to a new, multi-branch structure. The master branch will be kept in a canonical, deployable state, and the next branch will be where new development will go. This way, downtime will be minimized.

The `next` branch, when the naming change is complete, will be at pmm-next.herokuapp.com, while the `master` branch is at mango-melon-p4200.herokuapp.com.

## Notices:

(c) 2017 jack-the-coder. All rights reserved, except those waived by the Apache2 license.

See the LICENSE file at the root of this repository for more information.

Some of the code for this project is originally from TDIC by Omar Elamri (@eado). See thunderdynamics/tdic for more information.
