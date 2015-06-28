show_modal = (header_text, body, footer)->
  container = $('#main-modal')
  header = container.find('.uk-modal-header')
  if header_text
    header.html('<h1>'+header_text+'</h1>')
    header.show()
  else
    header.hide()
  dialog = container.find('.uk-modal-dialog')
  dialog.append(body)
  modal.show()
  return

close_modal = ->
  modal.hide()

clear_modal = ->
  mod = $('#main-modal')
  header = mod.find('.uk-modal-header')
  header.html ''
  dialog = mod.find('.uk-modal-dialog')
  dialog.html '<a class="uk-modal-close uk-close"></a><div class="uk-modal-header"></div>'

$('.new-rent').on('click', ->
  container_id = $(@).data('container')
  $.get('/period_form/', {container_id: container_id}, (data)->
    show_modal('Новый период аренды', data)
  )

  return
)

$('#main-modal').on('click', '#submit-period-form', ->
  my_form = $('#add-period-form')
  console.log(my_form)
  my_form.ajaxSubmit({
    error: ->
      alert('Произошла ошибка')
    success: (data, status) ->
      if data == 'OK'
        alert('Контейнер успешно поставлен в аренду')
        location.reload()
      else
        clear_modal()
        show_modal('Новый период аренды', data)
  })
  return false
)

$('#main-modal').on(
  'hide.uk.modal': ->
    header = $(@).find('.uk-modal-header')
    header.html ''
    dialog = $(@).find('.uk-modal-dialog')
    dialog.html '<a class="uk-modal-close uk-close"></a><div class="uk-modal-header"></div>'
)