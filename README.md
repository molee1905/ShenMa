ShenMa for Sublime Text 3
=============================
### Intro
This is a scaffold just for self-learning (e.g. how to create a sublime plugin and distribute it).During using [SublimeLinter][1],when i tried to create a linter plugin, i found this in its source code. This plugin is just extracted from [Sublimelinter][1]'s command named *SublimelinterCreateLinterPluginCommand*.

### Usage
There are two ways leading you to create a new sc from st3:
* Command Palette
    1. press ``shift+cmd+p``
    2. type ``create sc``, and choose the command
* Use Shortcut
    1. press ``ctrl+cmd+n``

then, you will be required to input `sc name` from the the input panel at the bottom of sublime, for the first time when you use, you will be required to input `sc path` too.

**For example:**
if you want to create a sc named *`news_info`*, and your sc path is *`$HOME/xxx/sc/shortcuts`*, you may see:

`please input shortcut path:` */Users/jack/xxx/sc/shortcuts*
`please intpu sc name:` *news_info*


tips: for now,  this plugin only works on  *OS X*

###License
[MIT][2]
[1]: https://github.com/SublimeLinter/SublimeLinter3
[2]: http://opensource.org/licenses/MIT