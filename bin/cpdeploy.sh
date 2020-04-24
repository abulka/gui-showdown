DEST=docs

mkdir -p $DEST/js
mkdir -p $DEST/css
mkdir -p $DEST/images

cd src/javascript
DEST=../../docs
cp -v \
index.html \
main_ecs.html \
main_oo.html \
main_plain.html \
main_vue.html  \
main_mvca.html  \
$DEST

# cp -v main_oo.py observer_oo.py test_observer_oo.py \
# main_ecs.py esper_observer.py esper.py \
# gui.py \
# ~/Devel/abulka.github.io/gui-showdown/python-implementation

# cp -v wx_esper.fbp \
# ~/Devel/abulka.github.io/gui-showdown/python-implementation/gui_via_wxformbuilder.fbp

# cp -v "README for deploy.md" \
# ~/Devel/abulka.github.io/gui-showdown/python-implementation/README.md

cd js
DEST=../../../docs/js
cp -v \
assert.js \
jecs_2.0.0_min.js \
main_ecs.js \
main_oo.js \
main_mvca.js \
observer_oo.js \
observer_events.js \
main_plain.js \
main_vue.js \
syntax_highlighting.js \
$DEST

cd ../css
DEST=../../../docs/css
cp -v \
main.css \
$DEST

cd ../images
DEST=../../../docs/images
cp -vR * \
$DEST

echo
echo "Access at
https://abulka.github.io/gui-showdown/index.html 
"
