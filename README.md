#ShenMa for Sublime Text 3
---------------------------

A plugin for shenma

### Intro
It's a plugin to create projects skeleton based on defined scaffolds, in my work, i call these projects "sc card" (shortcut). Through this plugin, for example when you input `news_detail`, it will generates folders(black) and files(italic) like below: 
* **news_detail**
  * **css**
      * *sc_advanced_news_detail.css*
  * **data**
  * **img**
  * **js**
      * *sc_news_detail.js*
  * **res**
  * **tmpl**
  * *.eslintrc*
  * *index.html*
  * *README.md*

the folders mentioned just now  will be appeared in your input path  (e.g. `/Users/jack/test/sc/shortcuts/`), and the `news_detail` is called **sc name**, the destination of the folder is called **sc path**

### Usage
There are two ways leading you to create a new sc from st3:
* Command Palette
    1. press `shift+cmd+p` 
    2. type `create sc`, and choose the command
* Use Shortcut
    1. press `ctrl+cmd+n`

then, you will be required to input `sc name` from the the input panel at the bottom of sublime, for the first time when you use, you will be required to input `sc path` too.

`please input shortcut path:` */Users/jack/xxx/sc/shortcuts/*
`please input sc name:` *news_detail*

---

This plugin also add a command to create `eslint.sublimt-build` to fix your javascript:
  1. press `shift+cmd+p` 
  2. type `Fix js`,  and choose the command
  3. `cmd+b`
of couse, first of all, you should make sure eslint has been installed, and eslint path is in `ShenMa.sublime-settings` which finally looks like below:

(`Preferences->Package Settings->ShenMa->Settings-User`)
```json
  {
    "eslint": "/usr/local/node/v0.12.7/bin",
    "shortcuts": "/Users/jack/test/sc/shortcuts"
  }

```

`Tips:` for now,  this plugin only works on *st3* and *OS X*

###License
[MIT][2]
[1]: https://github.com/SublimeLinter/SublimeLinter3
[2]: http://opensource.org/licenses/MIT

