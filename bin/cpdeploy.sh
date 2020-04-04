# DEST=~/Devel/abulka.github.io/gui-showdown
DEST=docs
# cp -v index.html $DEST
echo need to update this script to copy into docs dir instead and deploy as github page
exit 1




cp -v main_oo.py observer_oo.py test_observer_oo.py \
main_ecs.py esper_observer.py esper.py \
gui.py \
~/Devel/abulka.github.io/gui-showdown/python-implementation

cp -v wx_esper.fbp \
~/Devel/abulka.github.io/gui-showdown/python-implementation/gui_via_wxformbuilder.fbp

cp -v "README for deploy.md" \
~/Devel/abulka.github.io/gui-showdown/python-implementation/README.md

cd js/jecs

cp -v assert.js index.html jecs_extras.js jecs_min.js jecs.js \
main_ecs.html main_ecs.js \
nested_dict_accessor.js \
main_oo.html main_oo.js \
observer_oo.js observer_events.js \
main_plain.html main_plain.js \
main_vue.html main_vue.js \
main.css \
syntax_highlighting.js \
~/Devel/abulka.github.io/gui-showdown

cp -vR images/* ~/Devel/abulka.github.io/gui-showdown/images

echo
echo "Now cd into ~/Devel/abulka.github.io/gui-showdown, git commit, git push 
Then access with
https://abulka.github.io/gui-showdown/index.html 
"
