var app = (function () {

  // Instantiating engine, timer and simulator
  var engine = new Jecs.Engine();
  
  engine.on('tick:before', (engine) => {
    log_clear()
  })

  // 
  // Model - of a sort ;-)
  //

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
  message.setComponent('displayOptions', { upper: false })
  firstname.setComponent('displayOptions', { upper: false })
  surname.setComponent('displayOptions', { upper: false })
  topright.setComponent('displayOptions', { upper: false })


  // App - Set Model

  function set_message(val) {
    message.getComponent('data').val = val
  }
  function set_firstname(val) {
    firstname.getComponent('data').val = val
  }
  function set_surname(val) {
    surname.getComponent('data').val = val
  }

  // App - Toggle Model

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

  // App - Display Option Checkbox toggles

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
  
  function display_option_toggle_verbose_debug(flag) {
    flag ? $('#log-cont').show() : $('#log-cont').hide()
  }

  let $topleft = $('#welcome')
  let $topright = $('#welcome-user')




  // Systems

  engine.system('controller-model', ['data'], (entity, { data }) => {
    if (entity.name == 'model-welcome-message') $('input[name=welcome]').val(data.val)
    else if (entity.name == 'model-firstname') $('input[name=firstname]').val(data.val)
    else if (entity.name == 'model-surname') $('input[name=surname]').val(data.val)
    log(`controller-model: ${entity.name}, ${data.val}`);
  });

  engine.system('pre-render-topright', ['data', 'displayOptions'], (entity, { data, displayOptions }) => {
    let buffer = topright.getComponent('renderData')
    if (entity.name == 'model-welcome-message')
      buffer.welcome = displayOptions.upper ? data.val.toUpperCase() : data.val
    else if (entity.name == 'model-firstname')
      buffer.firstname = displayOptions.upper ? data.val.toUpperCase() : data.val
    else if (entity.name == 'model-surname')
      buffer.surname = displayOptions.upper ? data.val.toUpperCase() : data.val
    log(`pre-render-topright: model=${data.val} buffer: ${JSON.stringify(buffer)}, ${JSON.stringify(displayOptions)}`);
  });

  engine.system('controller-topleft', ['data', 'displayOptions'], (entity, { data, displayOptions }) => {
    if (entity.name == 'model-welcome-message')
      $topleft.html(displayOptions.upper ? data.val.toUpperCase() : data.val)
    log(`controller-topleft: ${entity.name}, ${data.val}, ${JSON.stringify(displayOptions)}`);
  });

  engine.system('controller-topright', ['renderData', 'displayOptions'], (entity, { renderData, displayOptions }) => {
    let s = `${renderData.welcome} ${renderData.firstname} ${renderData.surname}`
    if (displayOptions.upper)
      s = s.toUpperCase()
    $topright.html(s)
    log(`controller-topright: ${entity.name}, ${JSON.stringify(renderData)}, ${JSON.stringify(displayOptions)}`);
  });

  // world.system('controller-render-debug-dump', ['c_debug_dump_options'], (entity, {c_debug_dump_options}) => {  // For debugging
  //   let part1_html = syntaxHighlight(JSON.stringify({
  //     model: model, 
  //     // "entity_welcome[c_display_options]": entity_welcome.components.c_display_options,
  //     // "entity_welcome_user[c_display_options]": entity_welcome_user.components.c_display_options,
  //   }, null, 2))
  //   // let part2_html = dump_world(world, c_debug_dump_options.verbose)
  //   let part2_html = ""
  //   c_debug_dump_options.$el.html(part1_html + '<br>' + part2_html)
  // });
  
  engine.on('tick:after', (engine) => {
    let part1_html = syntaxHighlight(JSON.stringify({message, firstname, surname, topright} , null, 2))
    // let part2_html = dump_world(world, c_debug_dump_options.verbose)
    let part2_html = ""    
    $('#debug_info').html(part1_html + '<br>' + part2_html)
  })

  // Util - Logging

  var logarea = document.getElementById('log');

  // Append a line of log
  function log(text) {
    let pad = '&nbsp;'.repeat(30)
    text = text.replace('\n', `<br/>${pad}`)
    var html = logarea.innerHTML;
    html += (text || '') + '<br/>';
    logarea.innerHTML = html;

    // Scroll log to bottom
    // logarea.scrollTop = logarea.scrollHeight;
  }
  function log_clear() {
    logarea.innerHTML = ""
    // logarea.scrollTop = logarea.scrollHeight;
  }

  // Util - Uppercase

  function isUpperCaseAt(str, n) {
    return str[n] === str[n].toUpperCase();
  }

  function toggleCase(str) {  // determine case of string based on arbitrary choice of char 1
    return isUpperCaseAt(str, 1) ? str.toLowerCase() : str.toUpperCase()
  }

  // Boot

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

    display_option_toggle_verbose_debug,

    engine,
  }

}());
