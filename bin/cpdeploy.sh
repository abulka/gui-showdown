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
