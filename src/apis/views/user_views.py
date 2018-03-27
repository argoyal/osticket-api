from services import UserService
from flask import request, jsonify
from apis.forms import UserForm
from apis.decorators import private


user_service = UserService()


@private
def user_list():
    if request.method == "GET":
        """
        currently only supports email
        """
        email = request.args.get("email")

        if not email:
            return jsonify({
                "detail": "email is a required query param"
            }), 400

        return jsonify(user_service.get_user(email=email))

    if request.method == "POST":
        form = UserForm(request.json)

        if not form.is_valid():
            return jsonify({"detail": form.errors}), 400

        try:
            output = form.save(form.validated_data)

            return jsonify(output)
        except Exception as exc:
            return jsonify({"detail": repr(exc)}), 400
