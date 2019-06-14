from flask import jsonify, request, render_template, get_flashed_messages, flash
from werkzeug.exceptions import BadRequest
from app.constants import STATUS_ERROR, STATUS_OK


class Mixin:

    def render_response(self, context):
        raise NotImplementedError()

    @classmethod
    def get_inputs(cls):
        raise NotImplementedError()


class ApiMixin(Mixin):

    def render_response(self, context=None):
        if context is None:
            context = {}

        status = STATUS_OK
        messages = []

        for message in get_flashed_messages(with_categories=True):
            print(message)
            if message[0] == 'danger':
                status = STATUS_ERROR

            messages.append(message[1])

        context.update({'status': status, 'messages': messages})
        return jsonify(context)

    @classmethod
    def get_inputs(cls):
        inputs = {}

        try:
            inputs = request.get_json(force=True)
        except BadRequest:
            flash('Invalid Input.', 'danger')

        return inputs


class HtmlMixin:
    template_class = ''

    def render_response(self, context=None):
        if context is None:
            context = {}

        return render_template(self.template_class, **context)

    @classmethod
    def get_inputs(cls):
        return request.form
