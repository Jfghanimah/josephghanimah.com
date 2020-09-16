from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(403)
@errors.app_errorhandler(404)
@errors.app_errorhandler(500)
def error(error):
    code = error.code
    context = {'code':code}

    if code == 404:
        context["message"] = "Oops! Page Not Found"
        context["description"] = "That page does not exist. Please try a different one."
    elif code == 403:        
        context["message"] = "You don't have permission to do that."
        context["description"] = "Please check your account and try again."
    elif code == 500:
        context["message"] = "Something went wrong!"
        context["description"] = "We're experiencing some trouble on our end. Please try again in the near future."
    else:
        context["message"] = error.name
        context["description"] = error.description

    return render_template('error.html',  **context), error.code # 404, 403, 500
 
