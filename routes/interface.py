from flask_smorest import Blueprint

blp = Blueprint("Interface", "interface", description="Operations on the app interface")

@blp.route("/")
def title():
    return "<p>Bank Account Simulator</p>"
#Remember to write the interface text in another file in the future.