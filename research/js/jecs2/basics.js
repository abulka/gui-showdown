// Andy revamp - Apr 2020 - "its gotta be simpler than my first attempt!"

var app = (function () {

  // Instantiating engine, timer and simulator
  var engine = new Jecs.Engine();

  // Declare entities - this is like the model, but without data - we attach that later, as 'components'
  const message = engine.entity('model-welcome-message');
  const firstname = engine.entity('model-firstname');
  const surname = engine.entity('model-surname');
  const topright = engine.entity('display-model-topright');

  // Associate the model entities to components.
  message.setComponent('data', { val: "Welcome" })
  firstname.setComponent('data', { val: "Sam" })
  surname.setComponent('data', { val: "Smith" })
  topright.setComponent('renderData', { welcome:"", firstname:"", surname:"" })

  // we need display option re uppercase for welcome, the whole user, and the 'welcome user' message (top right)
  // only the first is an entity, the second is a combo of two entities and the third is a combo of three
  message.setComponent('displayOptions', { upper: false })
  firstname.setComponent('displayOptions', { upper: false })
  surname.setComponent('displayOptions', { upper: false })
  topright.setComponent('displayOptions', { upper: false })

  // Set Model

  function set_message(val) {
    message.getComponent('data').val = val
  }
  function set_firstname(val) {
    firstname.getComponent('data').val = val
  }
  function set_surname(val) {
    surname.getComponent('data').val = val
  }

  // Toggle Model

  function toggle_message() {
    let data = message.getComponent('data')
    data.val = toggleCase(data.val)
  }

  function toggle_user() {
    let data = firstname.getComponent('data')
    data.val = toggleCase(data.val)
    data = surname.getComponent('data')
    data.val = toggleCase(data.val)
  }

  // Display Option Checkbox toggles

  function display_option_toggle_message_case(flag) {
    message.getComponent('displayOptions').upper = flag
  }

  function display_option_toggle_user_case(flag) {
    firstname.getComponent('displayOptions').upper = flag
    surname.getComponent('displayOptions').upper = flag
  }

  function display_option_toggle_topright_case(flag) {
    topright.getComponent('displayOptions').upper = flag
  }

  let $topleft = $('#welcome')
  let $topright = $('#welcome-user')

  engine.on('tick:before', (engine) => {
    log_clear()
  })

  engine.system('controller-render-model', ['data'], (entity, { data }) => {
    if (entity.name == 'model-welcome-message') $('input[name=welcome]').val(data.val)
    else if (entity.name == 'model-firstname') $('input[name=firstname]').val(data.val)
    else if (entity.name == 'model-surname') $('input[name=surname]').val(data.val)
    log(`render-model: ${entity.name}, ${data.val}`);
  });

  engine.system('pre-render-display', ['data', 'displayOptions'], (entity, { data, displayOptions }) => {
    let buffer = topright.getComponent('renderData')
    if (entity.name == 'model-welcome-message')
      buffer.welcome = displayOptions.upper ? data.val.toUpperCase() : data.val
    else if (entity.name == 'model-firstname')
      buffer.firstname = displayOptions.upper ? data.val.toUpperCase() : data.val
    else if (entity.name == 'model-surname')
      buffer.surname = displayOptions.upper ? data.val.toUpperCase() : data.val

    log(`pre-render-display: ${entity.name}, ${data.val} buffer: ${JSON.stringify(buffer)}, displayOptions=${JSON.stringify(displayOptions)}`);
  });

  engine.system('controller-render-display-topleft', ['data', 'displayOptions'], (entity, { data, displayOptions }) => {
    if (entity.name == 'model-welcome-message')
      $topleft.html(displayOptions.upper ? data.val.toUpperCase() : data.val)
    log(`render-display-topleft: ${entity.name}, ${data.val}, displayOptions=${JSON.stringify(displayOptions)}`);
  });

  engine.system('controller-render-display-topright', ['renderData', 'displayOptions'], (entity, { renderData, displayOptions }) => {
    let s = `${renderData.welcome} ${renderData.firstname} ${renderData.surname}`
    if (displayOptions.upper)
      s = s.toUpperCase()
    $topright.html(s)
    log(`render-display-topright: ${entity.name}, ${JSON.stringify(renderData)}, displayOptions=${JSON.stringify(displayOptions)}`);
  });


  // Util - Logging

  var logarea = document.getElementById('log');

  // Append a line of log
  function log(text) {
    var html = logarea.innerHTML;
    html += (text || '') + '<br/>';
    logarea.innerHTML = html;

    // Scroll log to bottom
    logarea.scrollTop = logarea.scrollHeight;
  }
  function log_clear() {
    logarea.innerHTML = ""
    logarea.scrollTop = logarea.scrollHeight;
  }

  // Util

  function isUpperCaseAt(str, n) {
    return str[n] === str[n].toUpperCase();
  }

  function toggleCase(str) {  // determine case of string based on arbitrary choice of char 1
    return isUpperCaseAt(str, 1) ? str.toLowerCase() : str.toUpperCase()
  }

  engine.tick()

  return {
    set_message,
    set_firstname,
    set_surname,

    toggle_message,
    toggle_user,

    display_option_toggle_message_case,
    display_option_toggle_user_case,
    display_option_toggle_topright_case,
    engine,
  }

}());
